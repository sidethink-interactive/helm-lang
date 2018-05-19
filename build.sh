# This is a temporary script until helm can bootstrap itself.
# ../helm-lang points to a copy of the repo https://github.com/sidethink-interactive/helm-lang-bootstrapping

# Generate code.
cd src
./gen_token_kinds.py
cd ..

# Compile.
../helm-lang/helm build src/main.helm

# Rename binary.
mv main helm