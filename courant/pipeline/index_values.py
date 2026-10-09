"""Write a compact, agent-readable index of verified values and signals (ids match verified.json order)."""
import json, sys
UD = sys.argv[1]
d = json.load(open(f'{UD}/verified.json'))
with open(f'{UD}/index.txt', 'w') as o:
    o.write('# VALUES  id | item | fiscal_year | value | unit_as_printed | doc p.page | definition_note\n')
    for i, v in enumerate(d['values']):
        if v['verified']:
            o.write(f"V{i} | {v['item']} | {v['fiscal_year']} | {v['value']} | {v['unit_as_printed']} | {v['doc']} p.{v['found_page']} | {v['definition_note'][:160]}\n")
    o.write('\n# SIGNALS  id | category | fiscal_year | doc p.page | summary\n')
    for i, s in enumerate(d['signals']):
        if s['verified']:
            o.write(f"S{i} | {s['category']} | {s['fiscal_year']} | {s['doc']} p.{s['found_page']} | {s['summary'][:220]}\n")
print('index written')
