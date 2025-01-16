{
  inputs = {
    utils.url = "github:numtide/flake-utils";
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs, utils }:
    utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
      in
      {
        devShells.default = pkgs.mkShell {
          packages = with pkgs; [
            python39Full
            python39Packages.pip
            python39Packages.platformdirs

            ruff
            djlint
          ];

          LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [ pkgs.stdenv.cc.cc.lib pkgs.file ];

          shellHook = /* bash */ ''
            set_if_unset() {
                if [ -z "$(eval \$$1)" ]; then
                    export "$1"="$2"
                fi
            }

            # Setting LD_LIBRARY_PATH can cause issues on non-NixOS systems
            if ! command -v nixos-version &> /dev/null; then
                unset LD_LIBRARY_PATH
            fi

            SOURCE_DATE_EPOCH=$(date +%s)
            VENV=.venv
            if [ -d $VENV ]; then
              source ./$VENV/bin/activate
            fi
            export PYTHONPATH=`pwd`/$VENV/${pkgs.python39Full.sitePackages}/:$PYTHONPATH
          '';
        };
      });
}
