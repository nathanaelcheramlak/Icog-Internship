from hyperon import MeTTa

metta = MeTTa()

while True:
    user = input()
    if user == 'exit':
        break

    user_atom = metta.parse_single(user)
    metta.space().add_atom(user_atom)

print(metta.space().get_atoms())
print(type(metta.space().get_atoms()))

# with open("test.metta") as f:
#     a = f.read()
#     print(len(a))

# # print(len(a))
# print(metta.run(a))