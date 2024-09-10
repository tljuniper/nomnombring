{ self, pkgs }:

pkgs.nixosTest {
  name = "nomnombring-backend";

  nodes.machine = { config, pkgs, ... }: {
    imports = [
      self.nixosModules.nomnombring
    ];
    tljuniper.services.nomnombring =
      let
        j = [{
          "title" = "Saure Bohnensuppe";
          "portion" = "4 Portionen";
          "time" = "40 Minuten";
          "ingredients" = [
            {
              "name" = "Bohnen";
              "description" = "breite";
              "amount" = "500 g";
            }
            {
              "name" = "Kartoffeln";
              "description" = "";
              "amount" = "500 g";
            }
          ];
          "id" = 1;
        }];
        recipesFile = pkgs.writeText "recipes.json" (builtins.toJSON j);
      in
      {
        enable = true;
        configFile = pkgs.writeText "config.ini" ''
          [DEFAULT]
          recipe_file = ${recipesFile}

          [BRING]
          user = mail@example.com
          password = super-secret-password
          key = used-by-webapp-to-access-bring-api
        '';

      };

    system.stateVersion = "24.05";
  };

  testScript = ''
    output = machine.succeed("systemctl cat nomnombring-backend.service")
    print(output)
    machine.wait_for_unit("nomnombring-backend.service")
    machine.wait_for_open_port(5000)
    output = machine.succeed("curl 0.0.0.0:5000/recipes")
    assert "Saure Bohnensuppe" in output, "Recipe list does not contain expected recipe"

    machine.wait_for_unit("nginx.service")
    machine.wait_for_open_port(5000)
    output = machine.succeed("curl localhost")
    # App always connects to host "rust" and requires JS, so not much we can check here
    assert "<title>NomNomBring</title>" in output, "Webapp does not show expected title"

  '';
}
