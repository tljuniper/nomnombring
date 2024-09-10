{
  description = "Server for importing multiple recipes into Bring! App";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-24.05";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    {
      nixosModules = {
        nomnombring = import ./module.nix;
      };
    } // flake-utils.lib.eachDefaultSystem (system:
      let
        overlay = final: prev: {
          nomnombring = self.packages.${system}.nomnombring;
          nomnombring-backend = self.packages.${system}.nomnombring-backend;
        };
        pkgs = import nixpkgs {
          inherit system;
          overlays = [ overlay ];
        };
      in
      {
        checks = {
          test = pkgs.callPackage ./test.nix { inherit self; };
        };

        packages.nomnombring = pkgs.callPackage ./frontend.nix { };
        packages.nomnombring-backend = pkgs.callPackage ./backend.nix { };

        devShells.default =
          let
            pythonWithPackages = pkgs.python3.withPackages (ps: with ps;
              [
                flask
                flask-cors
                requests
                setuptools
                waitress
              ]);
          in
          pkgs.mkShell {
            packages = with pkgs; [
              nodejs
              nodePackages.npm
              nodePackages."@vue/cli"
              nixpkgs-fmt
              nix-output-monitor
              pythonWithPackages
              black
            ];

            # Workaround: make vscode's python extension read the .venv
            # Might be necessary to run `Python -> Select interpreter` in vscode after this
            shellHook = ''
              venv="$(cd $(dirname $(which python)); cd ..; pwd)"
              ln -Tsf "$venv" .venv
            '';
          };
      });
}
