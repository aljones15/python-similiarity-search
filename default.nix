 with import <nixpkgs> {}; {
    
    python3Env = stdenv.mkDerivation { 
      name = "impurePython3Env";
      buildInputs = [
         python35
         python35Packages.virtualenv
         python35Packages.numpy
         python35Packages.django_2_0
         python35Packages.pandas
         python35Packages.pip 
      ];
      PYTHONPATH="/home/liminal18/.local/lib/python3.5/site-packages";
    };
}


