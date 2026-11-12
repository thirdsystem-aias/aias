-- Copied unchanged from papers/v0_42/tables_as_tabular.lua (branch t4-paper) for the v1.12 Coverage Paper A build
-- (scripts/build_paper_v1_12.py); the v1.12 tables have at most 21 rows.
-- tables_as_tabular.lua -- pandoc filter for the v0.42 paper build (scripts/build_paper_v0_42.py).
-- Renders every table as an unbreakable booktabs tabular inside a table block placed here if it fits ([htbp]) with a numbered
-- caption, instead of pandoc's longtable. The v0.42 tables are short (at most 10 rows); longtable's page breaking
-- does not account for floats placed on the same page, which let figures run into the footer in the synthetic
-- pre-flight. Columns whose cells are long (over 45 characters) wrap in a p{} column; a table wider than the text
-- block is scaled down to the text width (graphicx \resizebox).

local function render(blocks)
  local s = pandoc.write(pandoc.Pandoc(blocks), 'latex')
  return (s:gsub('%s*\n%s*', ' '))
end

local function cell_text(c)
  return pandoc.utils.stringify(c.contents)
end

local function row(r)
  local cells = {}
  for _, c in ipairs(r.cells) do
    table.insert(cells, render(c.contents))
  end
  return table.concat(cells, ' & ') .. ' \\\\'
end

function Table(tbl)
  local ncol = #tbl.colspecs
  local maxlen = {}
  for i = 1, ncol do maxlen[i] = 0 end
  local function scan(r)
    for i, c in ipairs(r.cells) do
      local n = utf8.len(cell_text(c)) or #cell_text(c)
      if n > maxlen[i] then maxlen[i] = n end
    end
  end
  for _, b in ipairs(tbl.bodies) do for _, r in ipairs(b.body) do scan(r) end end
  local nlong = 0
  for i = 1, ncol do if maxlen[i] > 45 then nlong = nlong + 1 end end
  local spec = {}
  for i, cs in ipairs(tbl.colspecs) do
    local a = tostring(cs[1])
    if maxlen[i] > 45 then
      spec[i] = string.format('>{\\raggedright\\arraybackslash}p{%.2f\\linewidth}', 0.62 / nlong)
    elseif a == 'AlignRight' then spec[i] = 'r'
    elseif a == 'AlignCenter' then spec[i] = 'c'
    else spec[i] = 'l' end
  end
  local out = {'\\begin{table}[htbp]', '\\centering', '\\small'}
  local cap = render(tbl.caption.long)
  if cap ~= '' then table.insert(out, '\\caption{' .. cap .. '}') end
  table.insert(out, '\\resizebox{\\ifdim\\width>\\linewidth\\linewidth\\else\\width\\fi}{!}{%')
  table.insert(out, '\\begin{tabular}{' .. table.concat(spec) .. '}')
  table.insert(out, '\\toprule')
  for _, r in ipairs(tbl.head.rows) do table.insert(out, row(r)) end
  table.insert(out, '\\midrule')
  for _, b in ipairs(tbl.bodies) do
    for _, r in ipairs(b.body) do table.insert(out, row(r)) end
  end
  table.insert(out, '\\bottomrule')
  table.insert(out, '\\end{tabular}')
  table.insert(out, '}')
  table.insert(out, '\\end{table}')
  return pandoc.RawBlock('latex', table.concat(out, '\n'))
end
