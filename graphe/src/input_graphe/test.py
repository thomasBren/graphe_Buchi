import spot
# Translate LTLf to Büchi.
f = spot.from_ltlf('(a U b) & Fc')
aut = f.translate('small', 'buchi', 'sbacc')
# Remove "alive" atomic propositions and print result.
print(spot.to_finite(aut).to_str('hoa'))