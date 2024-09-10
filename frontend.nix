{ pkgs, ... }:
pkgs.buildNpmPackage {
  pname = "nomnombring";
  version = "0.0.0";
  src = ./frontend;

  makeCacheWritable = true;
  npmDepsHash = "sha256-iTjNVa9prFMoGExyr1qwDWXbF/UVUxWzmNbMCDe66vg=";
  npmFlags = [ "--legacy-peer-deps" ];

  prePatch = ''
    cp ${./frontend/package-lock.json} ./package-lock.json
    chmod +w ./package-lock.json
  '';

  installPhase =
    ''
      cp -r dist/ $out
    '';

  meta = with pkgs.lib; {
    maintainers = with maintainers; [ tljuniper ];
    license = licenses.mit;
    description = "Simple webapp for selecting recipe items";
    homepage =
      "https://github.com/tljuniper/nomnombring";
  };
}
