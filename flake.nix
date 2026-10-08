{
  inputs = {
    utils.url = "github:numtide/flake-utils";
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    # the locked nixpkgs' twine rejects the metadata version written by current setuptools
    nixpkgs-twine.url = "github:nixos/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs, nixpkgs-twine, utils }:
    utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
      in
      {
        packages.default = pkgs.python312Packages.buildPythonPackage rec {
          pname = "barely";
          version = "1.2.3";

          src = pkgs.fetchPypi {
            inherit pname version;
            hash = "sha256-hOh/0YzdBzARUOZyhXihPgm1nV459JYJ0wdTDVPKVFQ=";
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
            (python39Full.withPackages (ps: with ps; [
              pip
              platformdirs
              build
            ]))
            nixpkgs-twine.legacyPackages.${system}.twine

            ruff
            djlint
          ];

          shellHook = /* bash */ ''
            set_if_unset() {
                if [ -z "$(eval \$$1)" ]; then
                    export "$1"="$2"
                fi
            }

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
