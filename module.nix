{ config, lib, pkgs, ... }:

with lib;
let
  cfg = config.tljuniper.services.nomnombring;

  # Not making this configurable for now as we can't change the backend URL
  # that's used by the frontend anyways
  backend_port = 5000;

  # TODO: double check if there's a better way than building the package in two
  # places like this, e.g. something like
  # frontend = pkgs.nomnombring;
  # frontend = inputs.nomnombring.packages.${config.nixpkgs.system}.nomnombring;
  # Must work with both local `nix flake check` and module import without
  # overlays from other flakes
  frontend = pkgs.callPackage ./frontend.nix {};
in
{

  options = {
    tljuniper.services.nomnombring = {
      enable = mkEnableOption "nomnombring service";

      configFile = mkOption {
        type = types.path;
        example = "/path/to/config.ini";
        description = "Config file with bring credentials and recipes";
      };
    };
  };

  config = mkIf cfg.enable {

    services.nginx.enable = true;
    services.nginx.virtualHosts."nomnombring" = {
      root = "${frontend}/";
    };

    networking.firewall.allowedTCPPorts = [
      80 # nginx
      backend_port
    ];

    systemd.services.nomnombring-backend =
      let
        appEnv = pkgs.python3.withPackages (p: with p; [ waitress (callPackage ./backend.nix { }) ]);
      in
      {
        description = "Backend for recipe app that connects to Bring!";
        after = [ "network.target" ];
        wantedBy = [ "multi-user.target" ];
        environment.NOMNOMBRING_BACKEND_SETTINGS = cfg.configFile;
        serviceConfig = {
          User = "nomnombring";
          ExecStart = lib.escapeShellArgs [
            "${appEnv}/bin/waitress-serve"
            "--host"
            "0.0.0.0"
            "--port"
            "${builtins.toString backend_port}"
            "--call"
            "nomnombring.main:create_app"
          ];
          Restart = "always";
        };
      };

    users.users.nomnombring = {
      isSystemUser = true;
      group = "nomnombring";
    };

    users.groups.nomnombring = { };

  };
}
