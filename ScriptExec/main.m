/*
    Copyright (c) 2003-2025, Sveinbjorn Thordarson <sveinbjorn@sveinbjorn.org>
    All rights reserved.

    Redistribution and use in source and binary forms, with or without modification,
    are permitted provided that the following conditions are met:

    1. Redistributions of source code must retain the above copyright notice, this
    list of conditions and the following disclaimer.

    2. Redistributions in binary form must reproduce the above copyright notice, this
    list of conditions and the following disclaimer in the documentation and/or other
    materials provided with the distribution.

    3. Neither the name of the copyright holder nor the names of its contributors may
    be used to endorse or promote products derived from this software without specific
    prior written permission.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
    ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
    WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
    IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
    INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
    NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
    PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
    WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
    ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
    POSSIBILITY OF SUCH DAMAGE.
*/

@import Cocoa;

#include <mach-o/dyld.h>
#include <sys/param.h>
#include <string.h>
#include <libgen.h>

BOOL isBundled(void) {
    char path[MAXPATHLEN];
    uint32_t path_size = sizeof(path);
    
    // Get absolute path to executable
    if (_NSGetExecutablePath(path, &path_size) != 0) {
        return NO;
    }
    
    // Resolve symlinks
    char realPath[MAXPATHLEN];
    if (realpath(path, realPath) == NULL) {
        return NO;
    }
    
    // Walk up the tree checking for structure
    // Expected: .../MyApp.app/Contents/MacOS/MyApp
    // NB: dirname() modifies string in place

    // Check if parent dir is "MacOS"
    char *parent = dirname(realPath); // /path/to/MyApp.app/Contents/MacOS
    if (strcmp(basename(parent), "MacOS") != 0) {
        return NO;
    }
    
    // Check if parent dir is "Contents"
    parent = dirname(parent); // /path/to/MyApp.app/Contents
    if (strcmp(basename(parent), "Contents") != 0) return NO;

    // Check if parent dir ends with ".app" suffix
    parent = dirname(parent); // /path/to/MyApp.app
    char *grandparent = basename(parent);
    size_t len = strlen(grandparent);
    if (len < 4 || strcmp(grandparent + len - 4, ".app") != 0) return NO;
    
    return YES;
}

#ifdef DEBUG
    void exceptionHandler(NSException *exception);

    void exceptionHandler(NSException *exception) {
        NSLog(@"%@", [exception reason]);
        NSLog(@"%@", [exception userInfo]);
        NSLog(@"%@", [exception callStackReturnAddresses]);
        NSLog(@"%@", [exception callStackSymbols]);
    }
#endif

int main(int argc, char *argv[]) {
    if (isBundled() == NO) {
        printf("This binary must run from an application bundle\n");
        exit(EXIT_FAILURE);
    }
#ifdef DEBUG
    NSSetUncaughtExceptionHandler(&exceptionHandler);
#endif
    return NSApplicationMain(argc,  (const char **)argv);
}
