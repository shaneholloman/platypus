# TODO for Platypus

* Use NSDictionaryController and bindings for all controls in main window and sub-controllers
* http://stackoverflow.com/questions/1276029/non-blocking-stdio
* Terminal output mode? https://github.com/migueldeicaza/SwiftTerm
* Use pseudo-ttys for line buffered output: http://stackoverflow.com/questions/12586555/controlling-an-interactive-command-line-utility-from-a-cocoa-app-trouble-with  --- Look at PseudoTTY class
* Refactor ScriptExec for clean view controller/task controller decoupling. It's currently a mess.
* Refactor status menu item menu generation from output to share code between ScriptExec and Platypus.app
* Find a way to support authenticated task termination
* New button-based interface type
* New OnChange Text Filter interface type
* Implement new Table View interface (CSV output?)
* Create Platypus tutorial videos, make them available online
* Overhaul the Services feature
* Fix issue with multiple AEOpen events for many opened files
* Async Status Menu script execution to prevent interface locking on main thread
* Fix broken file watching of script path
* Add syntax for Status Menu output mode that suppresses menu entirely
* Update Applescript input example to Python, instead of Perl
* Make Status Menu from script generation non-blocking
* Upgrade Sparkle version
* Convert MainMenu.nib to XML format
* platypus.rb brew formula to install command line tool
* Fix selection change when item is deleted from the Bundled Files List
* Performance optimization in the app build process (precompiled nib)


DONE * Harden CI testing for this old project
DONE * Create more automated tests for command line tool and document existing tests

* Update FAQ to answer question wrt relative interpreter path / bundling own interpreter
* Base64-encode ScriptExec binary to ensure that Apple's annoying notarization works.
* Add GitHub action to test install of platypus command line tool
* Update Uninstall Platypus script
