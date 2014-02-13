tcc_database_manager
====================

This Python script helps to add items to the TCC.db sqlite database, which is useful in a distributed environment where a blanket TCC file would not work properly.

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

If any additional arguments are passed to the script, it disregards them entirely.

**Examples**

* `$ /path/to/tcc_database.py kTCCServiceAddressBook com.apple.Finder`
* `$ sudo /path/to/tcc_database.py kTCCServiceAccessibility my.needy.Application`

Caveats
-------

The script only recognizes three service names:

* `kTCCServiceAddressBook` (Contacts)
* `kTCCServiceUbiquity` (iCloud)
* `kTCCServiceAccessibility` (Accessibility)

As far as I am aware, these are the only service names that show up in TCC.db.  I made the script exclusive of other options to ensure no mistaken entries are created.

Additionally, this script assumes that the user wants to grant permission to the specified application.  In a desire to simplify execution of the script, I chose to remove the ability to deny access.  Adding such an option should not be too difficult, though.

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
===========
Much of the code used in this script was copy/pasted and then adapted from the `tccmanager.py` script written by Tim Sutton and published to his GitHub repository at https://github.com/timsutton/scripts/tree/master/tccmanager.  We're very grateful to Tim for posting his code online freely; it has been very helpful to us.
