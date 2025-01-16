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
        packages.default = pkgs.python312Packages.buildPythonPackage rec {
          pname = "barely";
          version = "1.2.2";

          src = pkgs.fetchPypi {
            inherit pname version;
            hash = "sha256-/gliqfkPwnhZilFXltNXuOjQnJoJ9u0SnktqlLmRfTo=";
          };


          doCheck = false;

          pyproject = true;
          build-system = [ pkgs.python312Packages.setuptools ];

          propagatedBuildInputs = with pkgs.python312Packages; [
            pip
            click
            click-default-group
            coloredlogs
            mock
            pyyaml
            watchdog
            pillow
            gitpython
            pygments
            libsass
            pysftp
            livereload
            binaryornot
            jinja2
            mistune
            calmjs
          ] ++ [ pkgs.python312Full ];
        };

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
