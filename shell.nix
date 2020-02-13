{
  pkgsSrc ? <nixpkgs>,
  pkgs ? import pkgsSrc {},
}:

with pkgs;

stdenv.mkDerivation {
  name = "ctff-dev-env";
  buildInputs = [
    gnumake
    python3
    python3Packages.poetry
  ];
}
