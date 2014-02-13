tcc_database_manager
====================

This Python script helps to add items to the TCC.db sqlite database, which is useful in a distributed environment where a blanket TCC file would not work properly.

Contents
--------
* [Background](#background) - what this script addresses
* [Usage](#usage) - how to use this script on the command line
  * [Examples](#examples) - usage examples
  * [Finding Bundle IDs](#finding-bundle-ids) - how to supply the necessary bundle ID
* [Caveats](#caveats) - this script isn't perfect...
* [Annoyances](#annoyances) - difficulties with the TCC system as a whole
* [Technical](#technical) - workarounds for per-environment specifications
* [Attribution](#attribution) - thanks!

Background
----------

Many applications request permission to access any of a number of services, such as Contacts, Accessibility, and iCloud.  Apple stores your answer to these requests in a sqlite3 database, named TCC.db.

This poses a problem in a distributed environment, though.  We constantly add new applications to our systems, and having to recreate the TCC file for our template user every time would be tedious and potentially prone to error (what if you forgot one of the other applications?).  This script allows us to programmatically add new applications to the database during our post-maintenance cycle.  In our environment it's integrated in such a way that adding an entry to the TCC.db database is no more difficult than adding a single line of text to our command files.

Usage
-----

`$ /path/to/tcc_database.py serviceName bundleID`

Of course, help text is available.  Simply call the script with any of `h`, `-h`, `help`, `--help` to access it.

Short of the help option to provide usage information, the script requires two arguments to be passed to it:

1. The service name, e.g. "kTCCServiceAddressBook" (for Contacts)
2. The bundle ID of the application, e.g. "com.apple.Finder" (for Finder)
  * Note: See [Finding Bundle IDs](#finding-bundle-ids) below for information on finding the bundle ID of the application.

If any additional arguments are passed to the script, it disregards them entirely.

#### Examples

* `$ /path/to/tcc_database.py kTCCServiceAddressBook com.apple.Finder`
* `$ sudo /path/to/tcc_database.py kTCCServiceAccessibility my.needy.Application`

#### Finding Bundle IDs

As bundle IDs are the method Apple uses to manage its TCC databases, it's important to know how to find them for any application.  In general, they can be found in the application's `Info.plist` file.  If your application is located at `/Applications/MyAwesomeApp.app`, then the plist file will most likely be located at `/Applications/MyAwesomeApp.app/Contents/Info.plist`.  In particular, you'll need to search for the string corresponding to the key `CFBundleIdentifier`.

Brett Terpstra [detailed a shell script to help with this](http://brettterpstra.com/2012/07/31/overthinking-it-fast-bundle-id-retrieval-for-mac-apps/), which I will reproduce here for your convenience.  As bash is my primary shell, I put this into the end of my `~/.bash_profile` so I can call it easily at any time.

```bash
# Allows for searching of Bundle IDs by application name
# Written by Brett Terpstra
bid() {
	local shortname location

	# combine all args as regex
	# (and remove ".app" from the end if it exists due to autocomplete)
	shortname=$(echo "${@%%.app}"|sed 's/ /.*/g')
	# if the file is a full match in apps folder, roll with it
	if [ -d "/Applications/$shortname.app" ]; then
		location="/Applications/$shortname.app"
	else # otherwise, start searching
		location=$(mdfind -onlyin /Applications -onlyin ~/Applications -onlyin /Developer/Applications 'kMDItemKind==Application'|awk -F '/' -v re="$shortname" 'tolower($NF) ~ re {print $0}'|head -n1)
	fi
	# No results? Die.
	[[ -z $location || $location = "" ]] && echo "$1 not found, I quit" && return
	# Otherwise, find the bundleid using spotlight metadata
	bundleid=$(mdls -name kMDItemCFBundleIdentifier -r "$location")
	# return the result or an error message
	[[ -z $bundleid || $bundleid = "" ]] && echo "Error getting bundle ID for \"$@\"" || echo "$location: $bundleid"
}
```
Once this is in your source file, you can simply call it as a command and it will search for your application and return both the app's location and its bundle ID:
```
$ bid safari
/Applications/safari.app: com.apple.Safari
```

Caveats
-------

The script only recognizes three service names:

* `kTCCServiceAddressBook` (Contacts)
* `kTCCServiceUbiquity` (iCloud)
* `kTCCServiceAccessibility` (Accessibility)

As far as I am aware, these are the only service names that show up in TCC.db.  I made the script exclusive of other options to ensure no mistaken entries are created.

Additionally, this script assumes that the user wants to grant permission to the specified application.  In a desire to simplify execution of the script, I chose to remove the ability to deny access.  Adding such an option should not be too difficult, though.

Annoyances
----------

Disappointingly, there does not seem to be an easy way to simply find out whether an application will request access to one of these services without opening the application and navigating it to a point where it asks for permission.  We have been investigating methods of programmatically discerning which of our applications will prompt the user to access different services, but have thus far been unsuccessful.  If you happen to know anything about this, we'd greatly appreciate any ideas.

It is worth noting that Apple has a method of automatically allowing certain applications access to services.  For example, in OS X 10.9 "Mavericks", TextEdit will automatically gain access to the `kTCCServiceUbiquity` service during its first launch, without any sort of prompt to the user.  We contacted Apple about utilizing this apparent backdoor for our machines so that we could just allow all requests to Contacts access (which would not pose an issue in our environment, I promise), but they informed us that this ability is hardcoded into the OS and we cannot access it.

There is also the mysterious `tccutil` command.  Its man page states:
```
DESCRIPTION
     The tccutil command manages the privacy database, which stores decisions the user has made about whether apps may
     access personal data.

     One command is current supported:

     reset    Reset all decisions for the specified service, causing apps to prompt again the next time they access the ser-
              vice.
```
I wish that this utility could be used to add access to a particular service for a specified application, or to completely open a service up and automatically accept all requests to it, or to turn off the service entirely so requests don't even exist... but none of this is possible.  The command only resets all access requests to a given service.

Technical
---------

Apple in fact has multiple TCC.db database files in any given installation (though none of them exist until the appropriate service is requested access to).  There is one for each user, in their `~/Library/Application Support/com.apple.TCC` folder, and there is one root database, located in `/Library/Application Support/com.apple.TCC`.  The local databases (those in each user's directory) are responsible for Contacts access and iCloud access.  The settings for these applications are granted on a per-user basis this way.  However, Accessibility permissions are stored (and must be stored) in the `/Library/...` database.  I assume this is due to the nature of those types of applications that request Accessibility access (they are granted some freedoms to the machine that could potentially be undesirable, so administrative access is required to add them).

This script will add Accessibility requests to the `/Library/...` database (assuming it is run with root permissions).  The other requests will be added to the TCC database file located at `/System/Library/User Template/English.lproj/Library/Application Support/com.apple.TCC/TCC.db`.  This is Apple's default template directory, from which all other user directories are created.

If you would prefer a different default location, such as the current user's home directory, the easiest solution would be to change the line

`options['local_dir'] = os.path.expanduser('/System/Library/User Template/English.lproj/Library/Application Support/com.apple.TCC')`

to

`options['local_dir'] = os.path.expanduser('~/Library/Application Support/com.apple.TCC')`

Python will automatically expand the path appropriately with the tilde.

Attribution
-----------

Much of the code used in this script was copy/pasted and then adapted from the `tccmanager.py` script written by Tim Sutton and published to his [GitHub repository](http://github.com/timsutton/scripts/tree/master/tccmanager).  We're very grateful to Tim for posting his code online freely; it has been very helpful to us.

Also, as mentioned above, thanks to Brett Terpstra for publishing his function to find bundle IDs online [at his website](http://brettterpstra.com/2012/07/31/overthinking-it-fast-bundle-id-retrieval-for-mac-apps/).
