"""AIAS v0.44 industry-breadth wave: brand registries (DRAFT r0).

Writes one CSV per industry to osf/v44/registries/, plus excluded_v0_44.csv and
industries_v0_44.csv. Every unit carries the dated public source it rests on
(URL, source date, access date 2026-11-10). Tier rule (PRE_REGISTRATION_v0_44 §3.2):
units are ordered by the source metric after the eligibility rules; L = eligible
ranks 1-6, C = eligible ranks 7-14, S = eligible ranks 15+ (all of them, or a
systematic sample where stated), G = ghost (a brand that left the US market in a
dated public event). No brand is chosen by hand outside these rules.

Run: python3 make_registries_v0_44.py   (stdlib only; deterministic)
"""
import csv, os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, '..', 'registries'))
ACCESSED = '2026-11-10'

SRC = {
    'NAIC24': ('NAIC 2025 Market Share report: top 25 private passenger auto groups by 2024 direct premiums written (table reproduced by Agency Checklists)',
               'https://agencychecklists.com/2025/03/17/naic-2025-market-share-top-25-private-passenger-auto-insurers-74894/', '2025-03-17', '2024'),
    'NAIC25': ('NAIC 2025 market share data, top 7 auto groups (Repairer Driven News); confirms the top-7 order for 2025',
               'https://www.repairerdrivennews.com/2026/03/31/state-farm-progressive-hold-37-of-auto-insurance-market-share-naic-data-shows/', '2026-03-31', '2025'),
    'ESUR': ('Insurance Journal, "Allstate to Retire Esurance Brand" (brand phased out in 2020)',
             'https://insurancejournal.com/news/national/2019/12/19/552548.htm', '2019-12-19', 'event'),
    'SH': ('ScrapeHero, 10 largest hotel chains in the USA by number of US locations',
           'https://www.scrapehero.com/location-reports/10-largest-hotels-in-the-usa/', '2026-10-16', '2025-11 to 2026-10 (per chain)'),
    'H325': ('HOTELS magazine, HOTELS 325 ("The List 2026", July/August 2026 issue), rooms at end of 2025',
             'https://hotelsmag.com/wp-content/uploads/2026/07/The-List-2026-4.pdf', '2026-07', '2025'),
    'NRF': ('NRF Top 100 Retailers 2026 (with Kantar), 2025 US retail sales',
            'https://nrf.com/research-insights/top-retailers/top-100-retailers/top-100-retailers-2026-list', '2026-07', '2025'),
    'AP1': ('Britannica Money, Great Atlantic & Pacific Tea Company (second bankruptcy 2015; last stores closed or sold by November 2016)',
            'https://www.britannica.com/money/Great-Atlantic-and-Pacific-Tea-Company-Inc', 'undated', 'event'),
    'AP2': ('Supermarket News, "A&P\'s store banners, private labels sold" (A&P "now gone in name as well")',
            'https://www.supermarketnews.com/retail-financial/ap-s-store-banners-private-labels-sold', '2018-05-02', 'event'),
    'QSR': ('QSR 50 (2025 edition, QSR Magazine): 2024 US systemwide sales, table reproduced by FoodIndustry.com',
            'https://www.foodindustry.com/?p=9527', '2025-11-11', '2024'),
    'DCI': ('Drug Channels Institute, top 15 US pharmacies of 2025 by prescription revenue (figures as reported by Becker\'s Hospital Review)',
            'https://www.beckershospitalreview.com/pharmacy/top-15-pharmacies-by-2025-prescription-revenue/', '2026-03-17', '2025'),
    'DCI0': ('Drug Channels, "The Top 15 U.S. Pharmacies of 2025" (Rite Aid has closed all of its stores and liquidated)',
             'https://www.drugchannels.net/2026/03/the-top-15-us-pharmacies-of-2025-market.html', '2026-03-17', 'event'),
    'CSP': ('CSP, "Top 40 convenience-store chains ranked: a 2026 update" (store counts as of 2026-01-01)',
            'https://www.cspdailynews.com/mergers-acquisitions/top-40-convenience-store-chains-ranked-2026-update', '2026-03-23', '2026-01-01'),
    'IB': ('Interbrand Best Global Brands 2026, luxury brands (Retail Times report of the ranking)',
           'https://retailtimes.co.uk/the-luxury-category-experiences-significant-shifts-in-value-across-interbrands-best-global-brands-2026/', '2026-10-28', '2026'),
    'LYST': ('The Lyst Index, hottest brands Q3 2026 (ranks 1-20)',
             'https://www.lyst.co.uk/the-lyst-index/Q3-26/', '2026-Q3 (page undated)', '2026-Q3'),
}

COLS = ['industry', 'unit_id', 'brand', 'tier', 'eligible_rank', 'source_rank', 'source_entity',
        'metric', 'metric_value', 'metric_unit', 'data_period', 'source_key', 'source_title',
        'source_url', 'source_date', 'accessed', 'aliases', 'match_rule', 'mapping_basis',
        'samsung_group_owned', 'samsung_relationship_note', 'notes']

# Industry definitions: id, label, file, Phase B noun phrase, Phase B expert phrase,
# Phase A category word, tier metric, rule notes.
INDUSTRIES = [
    ('INS', 'Car insurance', 'ins_car_insurance', 'car insurance companies', 'insurance experts and consumer reviewers', 'car insurance',
     'Private passenger auto direct premiums written, 2024 (NAIC)', 'Consumer-facing brand of each NAIC group; AAA clubs pooled into one unit; S = all remaining eligible ranks 15-25.'),
    ('HOT', 'Hotel chains', 'hot_hotel_chains', 'hotel chains', 'travel experts and reviewers', 'hotel',
     'US locations (ScrapeHero, ranks 1-10), then rooms (HOTELS 325) for further US brand-owning companies', 'Master brand as named in the source; sub-brands are not aliases; management companies and consortia excluded; S = every 2nd of the remaining guest-facing brands in rooms order, starting with the first.'),
    ('GRO', 'Grocery store chains', 'gro_grocery_chains', 'grocery store chains', 'food and consumer experts', 'grocery store',
     '2025 US retail sales (NRF Top 100 2026)', 'Companies whose primary format is the supermarket or grocery store and whose name is a store banner; mass merchants, clubs and dollar stores excluded; S = all remaining.'),
    ('QSR', 'Fast-food chains', 'qsr_fast_food_chains', 'fast-food chains', 'food critics and reviewers', 'fast-food',
     '2024 US systemwide sales (QSR 50, 2025 edition)', 'S = QSR 50 ranks 20, 25, 30, 35, 40, 45, 50 (every 5th from rank 20).'),
    ('APR', 'Clothing and department stores', 'apr_clothing_department_stores', 'clothing and department store chains', 'fashion and shopping experts', 'clothing store',
     '2025 US retail sales (NRF Top 100 2026)', 'Department, off-price and specialty apparel retailers in the NRF list; namesake or flagship banner; S = all remaining.'),
    ('PHA', 'Pharmacies', 'pha_pharmacies', 'pharmacies', 'health and consumer experts', 'pharmacy',
     '2025 prescription revenue (Drug Channels Institute); NRF 2025 US retail sales for the two independent-pharmacy networks', 'Consumer-facing pharmacy brand of each ranked company; S = all remaining.'),
    ('CVF', 'Convenience stores and gas stations', 'cvf_convenience_fuel', 'convenience store and gas station chains', 'travel and consumer experts', 'convenience store',
     'US store count at 2026-01-01 (CSP Top 40)', 'Chain name as store banner; holdings, distributors and multi-banner operators excluded (banner not established from the source); oil-major fuel brands excluded (count covers company-operated sites only); S = all remaining.'),
    ('FAS', 'Fashion and luxury', 'fas_fashion_luxury', 'luxury fashion brands', 'fashion editors and stylists', 'fashion',
     'Interbrand Best Global Brands 2026 brand value (luxury), then Lyst Index Q3 2026 rank for brands not in Interbrand', 'Global sources (no US-only ranking found); ranks 1-8 from Interbrand by value, 9+ from Lyst order; S = all remaining.'),
]

# Units in source-metric order (eligible units only; tiers are computed from the order).
# (brand, source_rank, source_entity, metric_value, metric_unit, source_key, aliases, match_rule, mapping_basis, samsung_note, notes)
# match_rule: ci = case-insensitive whole-word match; cs = case-sensitive whole-word match
# (used where an alias is also a common word or place name).
B = 'brand name = source entity name'
UNITS = {
 'INS': [
  ('State Farm', '1', 'State Farm Grp', '18.87', '% share (DPW 67.75 $bn)', 'NAIC24', 'State Farm', 'ci', B, '', '2025 rank 1 (NAIC25)'),
  ('Progressive', '2', 'Progressive Grp', '16.73', '% share (DPW 60.05 $bn)', 'NAIC24', 'Progressive', 'cs', B, '', '2025 rank 2 (NAIC25)'),
  ('GEICO', '3', 'Berkshire Hathaway Grp', '11.63', '% share (DPW 41.76 $bn)', 'NAIC24', 'GEICO|Geico', 'ci', 'GEICO is the group\'s auto insurance brand (named in NAIC25)', '', ''),
  ('Allstate', '4', 'Allstate Ins Grp', '10.19', '% share (DPW 36.58 $bn)', 'NAIC24', 'Allstate', 'ci', B, '', ''),
  ('USAA', '5', 'United Serv Automobile Assn Grp', '6.17', '% share (DPW 22.14 $bn)', 'NAIC24', 'USAA', 'cs', B, '', ''),
  ('Farmers Insurance', '6', 'Farmers Ins Grp', '3.76', '% share (DPW 13.49 $bn)', 'NAIC24', 'Farmers Insurance|Farmers', 'cs', B, '', ''),
  ('Liberty Mutual', '7', 'Liberty Mut Grp', '3.27', '% share (DPW 11.74 $bn)', 'NAIC24', 'Liberty Mutual', 'ci', B, '', ''),
  ('Travelers', '8', 'Travelers Grp', '2.00', '% share (DPW 7.18 $bn)', 'NAIC24', 'Travelers|The Travelers', 'cs', B, '', ''),
  ('AAA', '9;14;18', 'Auto Club Enterprises Ins Grp; CSAA Ins Grp; Automobile Club MI Grp', '3.86', '% share, three AAA club groups pooled (1.80 + 1.33 + 0.73)', 'NAIC24', 'AAA|AAA Insurance|Auto Club', 'cs', 'three AAA club insurance groups share one consumer brand; placed at the rank of its largest group (9)', '', 'Pooled unit; eligible rank set by the largest group, not by the pooled share.'),
  ('American Family Insurance', '10', 'American Family Ins Grp', '1.72', '% share (DPW 6.17 $bn)', 'NAIC24', 'American Family Insurance|American Family|AmFam', 'ci', B, '', ''),
  ('Auto-Owners Insurance', '11', 'Auto Owners Grp', '1.44', '% share (DPW 5.18 $bn)', 'NAIC24', 'Auto-Owners|Auto Owners', 'ci', B, '', ''),
  ('Erie Insurance', '12', 'Erie Ins Grp', '1.39', '% share (DPW 5.01 $bn)', 'NAIC24', 'Erie Insurance|Erie', 'cs', B, '', ''),
  ('Nationwide', '13', 'Nationwide Corp Grp', '1.34', '% share (DPW 4.80 $bn)', 'NAIC24', 'Nationwide', 'cs', B, '', 'Lower-case "nationwide" is an adjective; case-sensitive.'),
  ('Mercury Insurance', '15', 'Mercury Gen Grp', '0.94', '% share (DPW 3.37 $bn)', 'NAIC24', 'Mercury Insurance|Mercury', 'cs', B, '', ''),
  ('Sentry Insurance', '16', 'Sentry Ins Grp', '0.86', '% share (DPW 3.10 $bn)', 'NAIC24', 'Sentry Insurance|Sentry', 'cs', B, '', ''),
  ('Kemper', '17', 'Kemper Corp Grp', '0.83', '% share (DPW 2.96 $bn)', 'NAIC24', 'Kemper', 'ci', B, '', ''),
  ('The Hartford', '19', 'Hartford Fire & Cas Grp', '0.65', '% share (DPW 2.34 $bn)', 'NAIC24', 'The Hartford', 'ci', B, '', 'Bare "Hartford" (a city) is not an alias.'),
  ('Markel', '20', 'Markel Grp', '0.45', '% share (DPW 1.61 $bn)', 'NAIC24', 'Markel', 'ci', B, '', ''),
  ('Amica', '21', 'Amica Mut Grp', '0.44', '% share (DPW 1.59 $bn)', 'NAIC24', 'Amica|Amica Mutual', 'ci', B, '', ''),
  ('COUNTRY Financial', '22', 'Country Ins & Fin Serv Grp', '0.44', '% share (DPW 1.59 $bn)', 'NAIC24', 'COUNTRY Financial|Country Financial', 'ci', B, '', ''),
  ('Shelter Insurance', '23', 'Shelter Ins Grp', '0.44', '% share (DPW 1.58 $bn)', 'NAIC24', 'Shelter Insurance', 'ci', B, '', ''),
  ('NJM Insurance', '25', 'New Jersey Manufacturers Grp', '0.43', '% share (DPW 1.53 $bn)', 'NAIC24', 'NJM|NJM Insurance|New Jersey Manufacturers', 'ci', B, '', ''),
 ],
 'HOT': [
  ('Hilton', '1', 'Hilton Group Hotels & Resorts', '6666', 'US locations', 'SH', 'Hilton', 'ci', B, '', ''),
  ('Marriott', '2', 'Marriott Group Hotels & Resorts', '6402', 'US locations', 'SH', 'Marriott|Marriott Bonvoy', 'ci', B, '', ''),
  ('Choice Hotels', '3', 'Choice International Group Hotels', '5873', 'US locations', 'SH', 'Choice Hotels|Choice Privileges', 'ci', B, '', 'House of brands (Comfort, Quality Inn and others); sub-brands are not aliases.'),
  ('Wyndham', '4', 'Wyndham Group Hotels and Resorts', '5861', 'US locations', 'SH', 'Wyndham', 'ci', B, '', 'House of brands; sub-brands are not aliases.'),
  ('IHG', '5', 'IHG Group Hotels & Resorts', '4079', 'US locations', 'SH', 'IHG|IHG Hotels|InterContinental Hotels Group|IHG One Rewards', 'cs', B, '', 'House of brands (Holiday Inn and others); sub-brands are not aliases.'),
  ('Best Western', '6', 'Best Western Group Hotels & Resorts', '2045', 'US locations', 'SH', 'Best Western', 'ci', B, '', ''),
  ('Hyatt', '7', 'Hyatt Group Hotels & Resorts', '940', 'US locations', 'SH', 'Hyatt', 'ci', B, '', ''),
  ('Sonesta', '8', 'Sonesta International Group Hotels & Resorts', '785', 'US locations', 'SH', 'Sonesta', 'ci', B, '', ''),
  ('Red Roof', '9', 'Red Roof Inn', '732', 'US locations', 'SH', 'Red Roof|Red Roof Inn|Red Roof Plus', 'ci', B, '', ''),
  ('Americas Best Value Inn', '10', 'Americas Best Value Inn', '444', 'US locations', 'SH', "Americas Best Value Inn|America's Best Value Inn", 'ci', B, '', ''),
  ('Motel 6', 'H325-27', 'G6 Hospitality', '102521', 'rooms (end 2025)', 'H325', 'Motel 6', 'ci', 'G6 Hospitality trades as Motel 6 / Studio 6; Motel 6 is the guest-facing name', '', 'Second source (HOTELS 325) used below ScrapeHero rank 10.'),
  ('Extended Stay America', 'H325-36', 'Extended Stay America', '66000', 'rooms (end 2025)', 'H325', 'Extended Stay America', 'ci', B, '', ''),
  ('Four Seasons', 'H325-57', 'Four Seasons Hotels & Resorts', '33000', 'rooms (end 2025, estimated by HOTELS)', 'H325', 'Four Seasons', 'cs', B, '', 'Headquartered in Canada; operates in the US.'),
  ('Westgate Resorts', 'H325-89', 'Westgate Resorts', '14500', 'rooms (end 2025)', 'H325', 'Westgate Resorts|Westgate', 'cs', B, '', ''),
  ('Margaritaville', 'H325-111', 'Margaritaville', '8720', 'rooms (end 2025)', 'H325', 'Margaritaville', 'ci', B, '', 'S sample: 1st of 11.'),
  ('Club Quarters', 'H325-139', 'Club Quarters', '4500', 'rooms (end 2025)', 'H325', 'Club Quarters', 'ci', B, '', 'S sample: 3rd of 11.'),
  ('stayAPT Suites', 'H325-156', 'stayAPT Suites', '3003', 'rooms (end 2025)', 'H325', 'stayAPT|stayAPT Suites', 'ci', B, '', 'S sample: 5th of 11.'),
  ('AKA', 'H325-163', 'AKA Hotel & Residences', '2400', 'rooms (end 2025)', 'H325', 'AKA Hotel|AKA Hotels|AKA Hotel Residences|AKA Residences', 'ci', B, '', 'S sample: 7th of 11. Bare "AKA" (also known as) is not an alias.'),
  ('GrandStay', 'H325-171', 'GrandStay Hospitality', '1739', 'rooms (end 2025)', 'H325', 'GrandStay', 'ci', B, '', 'S sample: 9th of 11.'),
  ('Freehand', 'H325-181', 'Freehand', '927', 'rooms (end 2025)', 'H325', 'Freehand|Freehand Hotels', 'cs', B, '', 'S sample: 11th of 11.'),
 ],
 'GRO': [
  ('Kroger', 'NRF-4', 'The Kroger Co.', '154.74', '$bn 2025 US retail sales', 'NRF', 'Kroger', 'ci', B, '', 'Company total includes non-grocery formats.'),
  ('Albertsons', 'NRF-10', 'Albertsons Companies', '81.77', '$bn 2025 US retail sales', 'NRF', 'Albertsons', 'ci', 'namesake banner of a multi-banner company (Safeway and others are not aliases)', '', ''),
  ('Publix', 'NRF-12', 'Publix Super Markets', '62.75', '$bn 2025 US retail sales', 'NRF', 'Publix', 'ci', B, '', ''),
  ('Aldi', 'NRF-14', 'Aldi', '58.36', '$bn 2025 US retail sales', 'NRF', 'Aldi|ALDI', 'ci', B, '', ''),
  ('H-E-B', 'NRF-16', 'H.E. Butt Grocery', '44.16', '$bn 2025 US retail sales', 'NRF', 'H-E-B|HEB', 'cs', 'H-E-B is the store banner of H.E. Butt Grocery', '', ''),
  ('ShopRite', 'NRF-28', 'Wakefern / ShopRite', '19.57', '$bn 2025 US retail sales', 'NRF', 'ShopRite|Shop Rite', 'ci', 'banner named in the NRF entry', '', ''),
  ('Hy-Vee', 'NRF-35', 'Hy-Vee', '14.19', '$bn 2025 US retail sales', 'NRF', 'Hy-Vee|HyVee', 'ci', B, '', ''),
  ('Wegmans', 'NRF-38', 'Wegmans Food Markets', '13.36', '$bn 2025 US retail sales', 'NRF', 'Wegmans', 'ci', B, '', ''),
  ('WinCo Foods', 'NRF-47', 'Winco Foods', '10.65', '$bn 2025 US retail sales', 'NRF', 'WinCo|WinCo Foods', 'ci', B, '', ''),
  ('Giant Eagle', 'NRF-48', 'Giant Eagle', '10.63', '$bn 2025 US retail sales', 'NRF', 'Giant Eagle', 'ci', B, '', ''),
  ('Sprouts Farmers Market', 'NRF-53', 'Sprouts Farmers Market', '8.81', '$bn 2025 US retail sales', 'NRF', 'Sprouts Farmers Market|Sprouts', 'cs', B, '', ''),
  ('Piggly Wiggly', 'NRF-78', 'Piggly Wiggly', '5.85', '$bn 2025 US retail sales', 'NRF', 'Piggly Wiggly', 'ci', B, '', ''),
  ("Raley's", 'NRF-80', "Raley's Supermarkets", '5.63', '$bn 2025 US retail sales', 'NRF', "Raley's|Raleys", 'ci', B, '', ''),
  ('Stater Bros.', 'NRF-86', 'Stater Bros Holdings', '4.81', '$bn 2025 US retail sales', 'NRF', 'Stater Bros|Stater Brothers', 'ci', B, '', ''),
  ('Grocery Outlet', 'NRF-91', 'Grocery Outlet', '4.69', '$bn 2025 US retail sales', 'NRF', 'Grocery Outlet', 'ci', B, '', ''),
  ('Weis Markets', 'NRF-92', 'Weis Markets', '4.69', '$bn 2025 US retail sales', 'NRF', 'Weis Markets|Weis', 'ci', B, '', ''),
  ('Ingles', 'NRF-94', 'Ingles', '4.50', '$bn 2025 US retail sales', 'NRF', 'Ingles|Ingles Markets', 'ci', B, '', ''),
  ('Schnucks', 'NRF-98', 'Schnucks', '4.10', '$bn 2025 US retail sales', 'NRF', 'Schnucks', 'ci', B, '', ''),
  ('Save A Lot', 'NRF-100', 'Save-A-Lot', '4.06', '$bn 2025 US retail sales', 'NRF', 'Save A Lot|Save-A-Lot', 'ci', B, '', ''),
 ],
 'QSR': [
  ("McDonald's", '1', "McDonald's", '53469', '$m 2024 US systemwide sales', 'QSR', "McDonald's|McDonalds", 'ci', B, '', 'QSR 50 2026 edition top 10 (EatThis, undated) has the same ten chains.'),
  ('Starbucks', '2', 'Starbucks', '30400', '$m 2024 US systemwide sales', 'QSR', 'Starbucks', 'ci', B, '', ''),
  ('Chick-fil-A', '3', 'Chick-fil-A', '22746', '$m 2024 US systemwide sales', 'QSR', 'Chick-fil-A|Chick fil A|Chickfila', 'ci', B, '', ''),
  ('Taco Bell', '4', 'Taco Bell', '16200', '$m 2024 US systemwide sales', 'QSR', 'Taco Bell', 'ci', B, '', ''),
  ("Wendy's", '5', "Wendy's", '12554', '$m 2024 US systemwide sales', 'QSR', "Wendy's|Wendys", 'ci', B, '', ''),
  ("Dunkin'", '6', "Dunkin'", '12468', '$m 2024 US systemwide sales', 'QSR', "Dunkin'|Dunkin|Dunkin' Donuts|Dunkin Donuts", 'ci', B, '', ''),
  ('Chipotle', '7', 'Chipotle', '11111', '$m 2024 US systemwide sales', 'QSR', 'Chipotle|Chipotle Mexican Grill', 'cs', B, '', 'Lower-case "chipotle" is a pepper; case-sensitive.'),
  ('Burger King', '8', 'Burger King', '10980', '$m 2024 US systemwide sales', 'QSR', 'Burger King', 'ci', B, '', ''),
  ('Subway', '9', 'Subway', '9653', '$m 2024 US systemwide sales', 'QSR', 'Subway', 'cs', B, '', ''),
  ("Domino's", '10', "Domino's", '9500', '$m 2024 US systemwide sales', 'QSR', "Domino's|Dominos|Domino's Pizza", 'cs', B, '', ''),
  ('Panda Express', '11', 'Panda Express', '6199', '$m 2024 US systemwide sales', 'QSR', 'Panda Express', 'ci', B, '', ''),
  ('Panera Bread', '12', 'Panera', '5819', '$m 2024 US systemwide sales', 'QSR', 'Panera|Panera Bread', 'ci', B, '', ''),
  ('Popeyes', '13', 'Popeyes', '5726', '$m 2024 US systemwide sales', 'QSR', "Popeyes|Popeye's", 'ci', B, '', ''),
  ('Pizza Hut', '14', 'Pizza Hut', '5500', '$m 2024 US systemwide sales', 'QSR', 'Pizza Hut', 'ci', B, '', ''),
  ('Jack in the Box', '20', 'Jack in the Box', '4396', '$m 2024 US systemwide sales', 'QSR', 'Jack in the Box', 'ci', B, '', 'S sample: rank 20.'),
  ("Culver's", '25', "Culver's", '3680', '$m 2024 US systemwide sales', 'QSR', "Culver's|Culvers", 'ci', B, '', 'S sample: rank 25.'),
  ('In-N-Out Burger', '30', 'In-N-Out Burger', '2175', '$m 2024 US systemwide sales', 'QSR', 'In-N-Out|In N Out|In-N-Out Burger', 'ci', B, '', 'S sample: rank 30.'),
  ('Crumbl', '35', 'Crumbl', '1435', '$m 2024 US systemwide sales', 'QSR', 'Crumbl|Crumbl Cookies', 'ci', B, '', 'S sample: rank 35.'),
  ('El Pollo Loco', '40', 'El Pollo Loco', '1096', '$m 2024 US systemwide sales', 'QSR', 'El Pollo Loco', 'ci', B, '', 'S sample: rank 40.'),
  ('Cava', '45', 'Cava', '954', '$m 2024 US systemwide sales', 'QSR', 'CAVA|Cava', 'cs', B, '', 'S sample: rank 45.'),
  ('Tim Hortons', '50', 'Tim Hortons', '776', '$m 2024 US systemwide sales', 'QSR', "Tim Hortons|Tim Horton's", 'ci', B, '', 'S sample: rank 50.'),
 ],
 'APR': [
  ('T.J. Maxx', 'NRF-15', 'TJX Companies', '46.30', '$bn 2025 US retail sales', 'NRF', 'T.J. Maxx|TJ Maxx|TJMaxx|TJX', 'ci', 'flagship banner of TJX Companies (Marshalls and HomeGoods are not aliases)', '', 'Company total covers all TJX banners.'),
  ('Ross Dress for Less', 'NRF-22', 'Ross Stores', '22.70', '$bn 2025 US retail sales', 'NRF', 'Ross Dress for Less|Ross Stores|Ross', 'cs', 'namesake banner', '', ''),
  ("Macy's", 'NRF-25', "Macy's", '21.68', '$bn 2025 US retail sales', 'NRF', "Macy's|Macys", 'ci', B, '', "Company total includes Bloomingdale's (not an alias)."),
  ('Nordstrom', 'NRF-33', 'Nordstrom', '14.90', '$bn 2025 US retail sales', 'NRF', 'Nordstrom', 'ci', B, '', ''),
  ("Kohl's", 'NRF-34', "Kohl's", '14.78', '$bn 2025 US retail sales', 'NRF', "Kohl's|Kohls", 'ci', B, '', ''),
  ('Gap', 'NRF-37', 'Gap', '13.43', '$bn 2025 US retail sales', 'NRF', 'Gap|Gap Inc', 'cs', B, '', 'Company total includes Old Navy (not an alias); lower-case "gap" is a common word.'),
  ('Burlington', 'NRF-45', 'Burlington', '11.48', '$bn 2025 US retail sales', 'NRF', 'Burlington|Burlington Coat Factory', 'cs', B, '', ''),
  ('Saks Fifth Avenue', 'NRF-51', 'Saks Global', '8.97', '$bn 2025 US retail sales', 'NRF', 'Saks Fifth Avenue|Saks', 'ci', 'namesake banner of Saks Global (Neiman Marcus and Bergdorf Goodman are not aliases)', '', ''),
  ('JD Sports', 'NRF-70', 'JD Sports', '6.37', '$bn 2025 US retail sales', 'NRF', 'JD Sports', 'ci', B, '', ''),
  ('Lululemon', 'NRF-71', 'Lululemon', '6.33', '$bn 2025 US retail sales', 'NRF', 'Lululemon|lululemon', 'ci', B, '', ''),
  ("Dillard's", 'NRF-73', "Dillard's", '6.27', '$bn 2025 US retail sales', 'NRF', "Dillard's|Dillards", 'ci', B, '', ''),
  ('JCPenney', 'NRF-77', 'J.C. Penney Company', '5.96', '$bn 2025 US retail sales', 'NRF', 'JCPenney|JC Penney|J.C. Penney|Penney', 'ci', B, '', ''),
  ("Victoria's Secret", 'NRF-82', "Victoria's Secret", '5.43', '$bn 2025 US retail sales', 'NRF', "Victoria's Secret|Victorias Secret", 'ci', B, '', ''),
  ('American Eagle', 'NRF-90', 'American Eagle', '4.70', '$bn 2025 US retail sales', 'NRF', 'American Eagle|American Eagle Outfitters', 'ci', B, '', ''),
  ('Urban Outfitters', 'NRF-93', 'Urban Outfitters', '4.63', '$bn 2025 US retail sales', 'NRF', 'Urban Outfitters', 'ci', B, '', ''),
  ('Abercrombie & Fitch', 'NRF-99', 'Abercrombie & Fitch', '4.09', '$bn 2025 US retail sales', 'NRF', 'Abercrombie & Fitch|Abercrombie and Fitch|Abercrombie', 'ci', B, '', ''),
 ],
 'PHA': [
  ('CVS Pharmacy', 'DCI-1', 'CVS Health', '119.0', '$bn 2025 Rx revenue', 'DCI', 'CVS|CVS Pharmacy|CVS Caremark', 'cs', 'consumer pharmacy brand of CVS Health', 'Samsung Bioepis (Samsung affiliate) supplies a private-label biosimilar to Cordavis, a CVS Caremark subsidiary (see DEVIATIONS Entry 0, Part C)', ''),
  ('Walgreens', 'DCI-2', 'Walgreens Boots Alliance', '90.8', '$bn 2025 Rx revenue', 'DCI', 'Walgreens', 'ci', 'consumer pharmacy brand', '', ''),
  ('Express Scripts', 'DCI-3', 'Express Scripts (Cigna)', '80.5', '$bn 2025 Rx revenue', 'DCI', 'Express Scripts', 'ci', B, 'Samsung Bioepis (Samsung affiliate) supplies a private-label biosimilar to Quallent, an Express Scripts subsidiary (DEVIATIONS Entry 0, Part C)', ''),
  ('Optum Rx', 'DCI-4', 'Optum Rx (UnitedHealth Group)', '50.0', '$bn 2025 Rx revenue', 'DCI', 'Optum Rx|OptumRx', 'ci', B, '', 'Bare "Optum" is not an alias.'),
  ('Walmart Pharmacy', 'DCI-5', 'Walmart', '36.8', '$bn 2025 Rx revenue', 'DCI', 'Walmart|Walmart Pharmacy', 'ci', 'company name used for its pharmacies', '', ''),
  ('Kroger Pharmacy', 'DCI-6', 'The Kroger Co.', '17.1', '$bn 2025 Rx revenue', 'DCI', 'Kroger|Kroger Pharmacy', 'ci', 'company name used for its pharmacies', '', 'Also a unit of the grocery registry (separate industry and frames).'),
  ('Health Mart', 'NRF-42', 'Health Mart Systems', '12.25', '$bn 2025 US retail sales (NRF; not Rx revenue)', 'NRF', 'Health Mart', 'ci', 'franchise network of independent pharmacies', '', 'Metric differs from the DCI rows; placed by dollar value.'),
  ('CenterWell Pharmacy', 'DCI-7', 'Humana (CenterWell)', '11.7', '$bn 2025 Rx revenue', 'DCI', 'CenterWell|CenterWell Pharmacy', 'ci', B, '', ''),
  ('Publix Pharmacy', 'DCI-8', 'Publix', '11.7', '$bn 2025 Rx revenue', 'DCI', 'Publix|Publix Pharmacy', 'ci', 'company name used for its pharmacies', '', 'Also a unit of the grocery registry.'),
  ('Albertsons Pharmacy', 'DCI-10', 'Albertsons Cos.', '11.3', '$bn 2025 Rx revenue', 'DCI', 'Albertsons|Albertsons Pharmacy', 'ci', 'namesake banner', '', 'Also a unit of the grocery registry.'),
  ('Good Neighbor Pharmacy', 'NRF-50', 'Good Neighbor Pharmacy', '9.74', '$bn 2025 US retail sales (NRF; not Rx revenue)', 'NRF', 'Good Neighbor Pharmacy', 'ci', 'network of independent pharmacies', '', 'Metric differs from the DCI rows; placed by dollar value.'),
  ('PANTHERx Rare', 'DCI-11', 'PANTHERx Rare Pharmacy', '8.0', '$bn 2025 Rx revenue', 'DCI', 'PANTHERx|PANTHERx Rare', 'ci', B, '', 'Specialty pharmacy.'),
  ('CarelonRx', 'DCI-12', 'Elevance Health (CarelonRx)', '6.8', '$bn 2025 Rx revenue', 'DCI', 'CarelonRx|Carelon Rx', 'ci', B, '', ''),
  ('Costco Pharmacy', 'DCI-13', 'Costco', '4.7', '$bn 2025 Rx revenue', 'DCI', 'Costco|Costco Pharmacy', 'ci', 'company name used for its pharmacies', '', ''),
  ('AcariaHealth', 'DCI-14', 'Centene (AcariaHealth/Foundation Care)', '4.5', '$bn 2025 Rx revenue', 'DCI', 'AcariaHealth|Acaria Health|Foundation Care', 'ci', 'the two specialty pharmacy names given in the source', '', ''),
 ],
 'CVF': [
  ('7-Eleven', 'CSP-1', '7-Eleven Inc.', '12700', 'stores (2026-01-01)', 'CSP', '7-Eleven|7 Eleven|7-11', 'ci', B, '', ''),
  ('Circle K', 'CSP-2', 'Alimentation Couche-Tard Inc.', '7308', 'stores (2026-01-01)', 'CSP', 'Circle K', 'ci', 'network banner of Couche-Tard in the US', '', ''),
  ("Casey's", 'CSP-3', "Casey's General Stores Inc.", '2921', 'stores (2026-01-01)', 'CSP', "Casey's|Caseys", 'ci', B, '', ''),
  ('Murphy USA', 'CSP-4', 'Murphy USA Inc.', '1800', 'stores (2026-01-01)', 'CSP', 'Murphy USA|Murphy Express', 'ci', B, '', ''),
  ('QuikTrip', 'CSP-7', 'QuikTrip Corp.', '1196', 'stores (2026-01-01)', 'CSP', 'QuikTrip|QT', 'cs', B, '', ''),
  ('Wawa', 'CSP-8', 'Wawa Inc.', '1189', 'stores (2026-01-01)', 'CSP', 'Wawa', 'ci', B, '', ''),
  ('ExtraMile', 'CSP-9', 'ExtraMile Convenience Stores LLC', '1174', 'stores (2026-01-01)', 'CSP', 'ExtraMile|Extra Mile', 'cs', B, '', ''),
  ('Kwik Trip', 'CSP-11', 'Kwik Trip', '919', 'stores (2026-01-01)', 'CSP', 'Kwik Trip|Kwik Star', 'ci', B, '', ''),
  ('Maverik', 'CSP-12', 'Maverik Inc.', '818', 'stores (2026-01-01)', 'CSP', 'Maverik', 'ci', B, '', ''),
  ('Sheetz', 'CSP-13', 'Sheetz', '815', 'stores (2026-01-01)', 'CSP', 'Sheetz', 'ci', B, '', ''),
  ("Love's", 'CSP-14', "Love's Travel Stops & Country Stores", '668', 'stores (2026-01-01)', 'CSP', "Love's Travel Stops|Love's", 'cs', B, '', 'Tie at rank 14 with United Pacific (excluded).'),
  ('Pilot Flying J', 'CSP-16', 'Pilot Co.', '658', 'stores (2026-01-01)', 'CSP', 'Pilot Flying J|Flying J|Pilot Travel Centers', 'ci', 'Pilot Co. operates Pilot and Flying J travel centers', '', 'Bare "Pilot" is not an alias.'),
  ('RaceTrac', 'CSP-18', 'RaceTrac', '611', 'stores (2026-01-01)', 'CSP', 'RaceTrac', 'ci', B, '', ''),
  ('Yesway', 'CSP-19', 'Yesway', '448', 'stores (2026-01-01)', 'CSP', 'Yesway', 'ci', B, '', 'Tie at rank 19 with Sunshine Gasoline Distributors (excluded).'),
  ("Stewart's Shops", 'CSP-22', "Stewart's Shops", '404', 'stores (2026-01-01)', 'CSP', "Stewart's Shops|Stewart's", 'ci', B, '', ''),
  ('Jacksons', 'CSP-28', 'Jacksons Food Stores Inc.', '324', 'stores (2026-01-01)', 'CSP', 'Jacksons|Jacksons Food Stores', 'cs', B, '', ''),
  ('Royal Farms', 'CSP-30', 'Royal Farms', '314', 'stores (2026-01-01)', 'CSP', 'Royal Farms', 'ci', B, '', ''),
  ('RaceWay', 'CSP-34', 'RaceWay', '244', 'stores (2026-01-01)', 'CSP', 'RaceWay', 'cs', B, '', 'Distinct from RaceTrac; case-sensitive.'),
  ('Brake Time', 'CSP-35', 'Brake Time Corner Market LLC', '243', 'stores (2026-01-01)', 'CSP', 'Brake Time', 'ci', 'store name in the listed company name', '', ''),
 ],
 'FAS': [
  ('Hermès', 'IB-15', 'Hermès', '45.2', '$bn brand value (Interbrand 2026)', 'IB', 'Hermès|Hermes', 'ci', B, '', ''),
  ('Louis Vuitton', 'IB-16', 'Louis Vuitton', '45.1', '$bn brand value (Interbrand 2026)', 'IB', 'Louis Vuitton', 'ci', B, '', ''),
  ('Chanel', 'IB-24', 'Chanel', '32.9', '$bn brand value (Interbrand 2026)', 'IB', 'Chanel', 'ci', B, '', 'Lyst Q3 2026 rank 2.'),
  ('Cartier', 'IB-69', 'Cartier', '12.2', '$bn brand value (Interbrand 2026)', 'IB', 'Cartier', 'ci', B, '', ''),
  ('Dior', 'IB-85', 'Dior', '8.9', '$bn brand value (Interbrand 2026)', 'IB', 'Dior|Christian Dior', 'ci', B, '', 'Lyst Q3 2026 rank 6.'),
  ('Tiffany & Co.', 'IB-91', 'Tiffany & Co', '8.1', '$bn brand value (Interbrand 2026)', 'IB', 'Tiffany & Co.|Tiffany & Co|Tiffany', 'cs', B, '', ''),
  ('Gucci', 'IB-93', 'Gucci', '8.1', '$bn brand value (Interbrand 2026)', 'IB', 'Gucci', 'ci', B, '', 'Lyst Q3 2026 rank 4.'),
  ('Prada', 'IB-96', 'Prada', '7.6', '$bn brand value (Interbrand 2026)', 'IB', 'Prada', 'ci', B, '', 'Lyst Q3 2026 rank 1.'),
  ('Miu Miu', 'LYST-3', 'Miu Miu', '3', 'Lyst Index rank', 'LYST', 'Miu Miu', 'ci', B, '', ''),
  ('Saint Laurent', 'LYST-5', 'Saint Laurent', '5', 'Lyst Index rank', 'LYST', 'Saint Laurent|Yves Saint Laurent|YSL', 'ci', B, '', ''),
  ('Burberry', 'LYST-7', 'Burberry', '7', 'Lyst Index rank', 'LYST', 'Burberry', 'ci', B, '', ''),
  ('Ralph Lauren', 'LYST-8', 'Ralph Lauren', '8', 'Lyst Index rank', 'LYST', 'Ralph Lauren|Polo Ralph Lauren', 'ci', B, '', ''),
  ('Chloé', 'LYST-9', 'Chloé', '9', 'Lyst Index rank', 'LYST', 'Chloé|Chloe', 'cs', B, '', ''),
  ('Celine', 'LYST-10', 'Celine', '10', 'Lyst Index rank', 'LYST', 'Celine|Céline', 'cs', B, '', ''),
  ('Bottega Veneta', 'LYST-11', 'Bottega Veneta', '11', 'Lyst Index rank', 'LYST', 'Bottega Veneta|Bottega', 'ci', B, '', ''),
  ('Coach', 'LYST-12', 'Coach', '12', 'Lyst Index rank', 'LYST', 'Coach', 'cs', B, '', 'Lower-case "coach" is a common word; case-sensitive.'),
  ('Massimo Dutti', 'LYST-13', 'Massimo Dutti', '13', 'Lyst Index rank', 'LYST', 'Massimo Dutti', 'ci', B, '', ''),
  ('The Row', 'LYST-14', 'The Row', '14', 'Lyst Index rank', 'LYST', 'The Row', 'cs', B, '', ''),
  ('Moncler', 'LYST-15', 'Moncler', '15', 'Lyst Index rank', 'LYST', 'Moncler', 'ci', B, '', ''),
  ('Dries Van Noten', 'LYST-16', 'Dries Van Noten', '16', 'Lyst Index rank', 'LYST', 'Dries Van Noten', 'ci', B, '', ''),
  ('Loewe', 'LYST-17', 'Loewe', '17', 'Lyst Index rank', 'LYST', 'Loewe', 'ci', B, '', ''),
  ('Diesel', 'LYST-18', 'Diesel', '18', 'Lyst Index rank', 'LYST', 'Diesel', 'cs', B, '', 'Lower-case "diesel" is a fuel; case-sensitive.'),
  ('Stone Island', 'LYST-19', 'Stone Island', '19', 'Lyst Index rank', 'LYST', 'Stone Island', 'ci', B, '', ''),
  ('Khaite', 'LYST-20', 'Khaite', '20', 'Lyst Index rank', 'LYST', 'Khaite', 'ci', B, '', ''),
 ],
}

# Ghosts: brands that left the US market in a dated public event (descriptive cell; not in H_Spread or H_Tier).
GHOSTS = {
 'INS': [('Esurance', 'event', 'Esurance (Allstate)', '2020', 'brand phased out', 'ESUR', 'Esurance', 'ci', B, '', 'Allstate announced 2019-12-19 that the brand would be phased out in 2020.')],
 'GRO': [('A&P', 'event', 'The Great Atlantic & Pacific Tea Company', '2015-2016', 'Chapter 11 (2015); last stores closed or sold by Nov 2016', 'AP1', 'A&P|A & P|Great Atlantic & Pacific Tea', 'cs', B, '', 'Banners and IP sold by 2018 (Supermarket News, 2018-05-02: ' + SRC['AP2'][1] + ').')],
 'PHA': [('Rite Aid', 'event', 'Rite Aid', 'by 2026-03-17 (source date)', 'had closed all stores and liquidated', 'DCI0', 'Rite Aid|RiteAid', 'ci', B, '', '')],
}

# Exclusions from the eligible lists (rank in source; reason).
EXCLUDED = [
 ('INS', 'Southern Farm Bureau Cas Grp', 'NAIC24 rank 24', 'The "Farm Bureau" name is shared by several separate state Farm Bureau insurers; a mention cannot be attributed to this group.'),
 ('INS', 'CSAA Ins Grp; Automobile Club MI Grp', 'NAIC24 ranks 14, 18', 'Pooled into the AAA unit (same consumer brand).'),
 ('HOT', 'Accor', 'H325 rank 6', 'No US count in the sources; global rooms would misplace it in a US registry.'),
 ('HOT', 'Third-party management companies (e.g. Aimbridge, Highgate, HEI, Remington, Concord, Crescent, Pyramid, HHM)', 'H325 various', 'Operate hotels under other companies\' brands; no guest-facing brand of their own.'),
 ('HOT', 'Consortia (Preferred Hotels & Resorts, The Leading Hotels of the World, Keytel, HotelREZ, Global Hotel Alliance)', 'H325 various', 'Marketing affiliations of independent hotels, not hotel brands.'),
 ('HOT', 'Marcus Hotels & Resorts; hihotels by Hospitality International', 'H325 ranks 136, 114', 'Operator or house of franchise brands with no single guest-facing name; removed before the S sample was drawn.'),
 ('HOT', 'Starwood Hotels (H325 rank 151)', 'H325 rank 151', 'Name collides with Starwood Hotels & Resorts, merged into Marriott in 2016; mentions cannot be attributed.'),
 ('HOT', 'Omni Hotels & Resorts; Loews Hotels', 'not in either source', 'Not listed in the sources used; no dated size figure.'),
 ('HOT', 'Shilla (The Shilla, Shilla Stay)', 'not in either US source', 'Samsung affiliate (Hotel Shilla); not a US brand in the sources; would be excluded on COI grounds in any case (DEVIATIONS Entry 0).'),
 ('GRO', 'Walmart; Costco; Target; BJ\'s Wholesale Club; Amazon.com; Meijer', 'NRF ranks 1, 3, 8, 26, 2, 21', 'Mass merchants, warehouse clubs, e-commerce or supercenters, not supermarket or grocery-store formats.'),
 ('GRO', 'Royal Ahold Delhaize USA; Northeast Grocery; Chedraui; My Demoulas', 'NRF ranks 13, 55, 57, 81', 'Company name is not a store banner; banner-level sales are not in the source.'),
 ('GRO', 'Dollar General; Family Dollar; Dollar Tree; 7-Eleven; Alimentation Couche-Tard; Casey\'s', 'NRF various', 'Dollar or convenience formats (convenience chains are in the CVF registry).'),
 ('GRO', 'Defense Commissary Agency', 'NRF rank 85', 'Government commissary system.'),
 ('GRO', 'Trader Joe\'s; Whole Foods Market', 'not separately listed in NRF 2026', 'No separate entry in the source (Whole Foods is within Amazon.com).'),
 ('QSR', 'QSR 50 ranks 15-19, 21-24, 26-29, 31-34, 36-39, 41-44, 46-49', 'QSR 50 2025', 'Not drawn by the systematic S sample (every 5th rank from 20).'),
 ('APR', 'Dick\'s Sporting Goods; Academy Sports; Bass Pro', 'NRF ranks 27, 76, 58', 'Sporting-goods retailers, not apparel or department stores.'),
 ('APR', 'Ulta Beauty; Sephora', 'NRF ranks 41, 52', 'Beauty retailers (cosmetics already measured by the programme).'),
 ('APR', 'Signet Jewelers; Bath & Body Works; Tapestry', 'NRF ranks 74, 65, 95', 'Jewelry or personal-care retailers, or a brand owner (Coach is a unit of the FAS registry).'),
 ('PHA', 'BrightSpring Health Services', 'DCI rank 9', 'Long-term-care and infusion pharmacy operator; no consumer pharmacy brand under that name.'),
 ('PHA', 'Ahold Delhaize (pharmacies)', 'DCI rank 15', 'Pharmacies operate under several store banners; no single pharmacy brand.'),
 ('CVF', 'bp America; Shell; Sunoco LP', 'CSP ranks 5, 31, 33', 'Oil-major fuel brands: the count covers company-operated sites only and misstates the brand\'s footprint.'),
 ('CVF', 'EG America; GPM Investments; United Pacific/Rocket; Anabi Oil; Sunshine Gasoline Distributors; United Refining; H&S Energy; Bolla Corp.; CrossAmerica Partners; The Cigarette Store Corp.; Global Partners; Nouria Energy; Majors Management; Refuel Operating; FEMSA; Par Mar Oil; G&M Oil', 'CSP various', 'Holding, distributor or multi-banner operator; the store banner is not established from the source.'),
 ('CVF', 'Meijer Gas Stations', 'CSP rank 36', 'Part of the Meijer supercenter chain.'),
 ('FAS', 'Nike; Zara; Uniqlo; H&M; Adidas', 'Interbrand 2026 (apparel, not luxury)', 'Mass-market apparel or sportswear (running shoes already measured); outside the luxury frame.'),
]


def article(word):
    return 'an' if word[0].lower() in 'aeiou' else 'a'


def main():
    os.makedirs(OUT, exist_ok=True)
    summary = []
    allrows = []
    for (iid, label, fname, noun, experts, catword, metric, rule) in INDUSTRIES:
        rows = []
        for n, u in enumerate(UNITS[iid], start=1):
            tier = 'L' if n <= 6 else ('C' if n <= 14 else 'S')
            rows.append((u, tier, str(n)))
        for u in GHOSTS.get(iid, []):
            rows.append((u, 'G', ''))
        out = []
        for k, (u, tier, er) in enumerate(rows, start=1):
            (brand, srank, sent, mval, munit, skey, aliases, mrule, mbasis, snote, notes) = u
            st, surl, sdate, period = SRC[skey]
            out.append({
                'industry': iid, 'unit_id': '%s%02d' % (iid, k), 'brand': brand, 'tier': tier,
                'eligible_rank': er, 'source_rank': srank, 'source_entity': sent,
                'metric': metric if tier != 'G' else 'exit event', 'metric_value': mval, 'metric_unit': munit,
                'data_period': period, 'source_key': skey, 'source_title': st, 'source_url': surl,
                'source_date': sdate, 'accessed': ACCESSED, 'aliases': aliases, 'match_rule': mrule,
                'mapping_basis': mbasis, 'samsung_group_owned': 'no', 'samsung_relationship_note': snote,
                'notes': notes})
        path = os.path.join(OUT, fname + '.csv')
        with open(path, 'w', newline='', encoding='utf-8') as f:
            w = csv.DictWriter(f, fieldnames=COLS, lineterminator='\n')
            w.writeheader()
            w.writerows(out)
        allrows += out
        cnt = {t: sum(1 for r in out if r['tier'] == t) for t in 'LCSG'}
        summary.append({'industry': iid, 'label': label, 'file': 'registries/' + fname + '.csv',
                        'units': len(out), 'L': cnt['L'], 'C': cnt['C'], 'S': cnt['S'], 'G': cnt['G'],
                        'phase_b_noun': noun, 'phase_b_experts': experts,
                        'phase_a_category': catword, 'phase_a_article': article(catword),
                        'tier_metric': metric, 'rule': rule})
    with open(os.path.join(OUT, 'industries_v0_44.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(summary[0].keys()), lineterminator='\n')
        w.writeheader()
        w.writerows(summary)
    with open(os.path.join(OUT, 'excluded_v0_44.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f, lineterminator='\n')
        w.writerow(['industry', 'excluded', 'source_position', 'reason'])
        w.writerows(EXCLUDED)
    # sanity: unique brand names within an industry
    for iid in UNITS:
        names = [r['brand'] for r in allrows if r['industry'] == iid]
        assert len(names) == len(set(names)), iid
    tot = sum(s['units'] for s in summary)
    for s in summary:
        print('%-4s %-38s units=%2d  L=%d C=%d S=%d G=%d' % (s['industry'], s['label'], s['units'], s['L'], s['C'], s['S'], s['G']))
    print('total units:', tot, '| industries:', len(summary))


if __name__ == '__main__':
    main()
