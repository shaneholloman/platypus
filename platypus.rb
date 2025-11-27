class Platypus < Formula
  desc "Command line tool to create macOS application bundles from command line scripts"
  homepage "https://sveinbjorn.org/platypus"
  url ""
  sha256 ""
  license "BSD-3-Clause"

  depends_on xcode: ["13.0", :build]

  def install
    # Fix hardcoded paths in Common.h to point to Homebrew's share directory
    # This ensures the 'platypus' tool can find 'ScriptExec' and 'MainMenu.nib'
    inreplace "Common.h" do |s|
      s.gsub! "/usr/local/share/platypus", pkgshare
    end

    # Build the command line tool and the helper app (ScriptExec)
    system "make", "clt"

    # Install the executable
    bin.install "products/platypus_clt" => "platypus"

    # Install the helper app and resources to #{pkgshare}
    pkgshare.install "products/ScriptExec"
    pkgshare.install "MainMenu.nib"

    # Install the man page
    man1.install "CLT/man/platypus.1"
  end

  test do
    system "#{bin}/platypus", "--version"
  end
end
