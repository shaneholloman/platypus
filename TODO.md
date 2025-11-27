# TODO for Platypus

* Use NSDictionaryController and bindings for all controls in main window and sub-controllers
* http://stackoverflow.com/questions/1276029/non-blocking-stdio
* Terminal output mode? https://github.com/migueldeicaza/SwiftTerm
* Use pseudo-ttys for line buffered output: http://stackoverflow.com/questions/12586555/controlling-an-interactive-command-line-utility-from-a-cocoa-app-trouble-with  --- Look at PseudoTTY class
* Refactor ScriptExec for clean view controller/task controller decoupling. It's currently an absolute mess.
* Refactor status menu item menu generation from output to share code between ScriptExec and Platypus.app
* Find a way to support authenticated task termination
* New button-based interface type
* New OnChange Text Filter interface type
* Implement new Table View interface (CSV output?)
* Create Platypus tutorial videos, make them available online
* Overhaul the Services feature
* Fix issue with multiple AEOpen events for many opened files
* Asynchronous Status Menu script execution to prevent interface blocking main thread
* Fix broken file watching of script path
* Add syntax for Status Menu output mode that suppresses menu entirely
* Migrate documentation examples to Python, instead of Perl (which nobody uses any more)
* Upgrade Sparkle version to 2.8.1
* Convert MainMenu.nib to modern XML format
* Create platypus.rb Homebrew formula to install command line tool
* Fix selection change when item is deleted from the Bundled Files List (select item above)
* Performance optimization in the app build process (also include precompiled nib)


DONE * Harden CI testing for this old project
DONE * Create more automated tests for command line tool and document existing tests
DONE * Add GitHub action to test install of platypus command line tool

* Update FAQ to answer question wrt relative interpreter path / bundling own interpreter
* Base64-encode ScriptExec binary to ensure that Apple's annoying notarization works.
    * Release as an Apple-notarized app
* Update Uninstall Platypus shell script so it works
