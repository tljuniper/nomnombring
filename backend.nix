{ pkgs, ... }:
with pkgs.python3Packages;
pkgs.python3Packages.buildPythonPackage {
  name = "nomnombring-backend";
  src = ./backend;

  propagatedBuildInputs = [
    flask
    flask-cors
    requests
    pip
    setuptools
  ];
  checkPhase = false;
}
