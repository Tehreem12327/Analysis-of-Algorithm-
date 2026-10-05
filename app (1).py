import random
import time

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Top Students Finder", page_icon="🏆", layout="wide")

# ---------------------------------------------------------------
# STYLING
# ---------------------------------------------------------------
st.markdown(
    """
<style>
.hero {
    background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
    padding: 28px 32px; border-radius: 16px; color: white; margin-bottom: 24px;
}
.hero h1 {margin: 0; font-size: 2.1rem; color: white;}
.hero p {margin: 6px 0 0 0; opacity: .9; font-size: 1.05rem;}
.step {
    font-weight: 700; font-size: 1.15rem; margin: 18px 0 8px 0; color: #4f46e5;
}
.podium {
    border-radius: 14px; padding: 18px; text-align: center; color: #1f2937;
    box-shadow: 0 2px 8px rgba(0,0,0,.12);
}
.podium .medal {font-size: 2.2rem;}
.podium .name {font-weight: 700; font-size: 1.1rem; margin-top: 4px;}
.podium .marks {font-size: 1.6rem; font-weight: 800;}
.gold {background: linear-gradient(135deg,#fde68a,#fbbf24);}
.silver {background: linear-gradient(135deg,#e5e7eb,#9ca3af);}
.bronze {background: linear-gradient(135deg,#fed7aa,#fb923c);}
</style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="hero">
  <h1>🏆 Top Students Finder</h1>
  <p>Upload your students’ file, choose a sorting algorithm and find the top students based on their marks.</p>
</div>
""",
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------
# SORTING ALGORITHMS
# Har algorithm (sorted_list, comparisons, swaps) return karta hai.
# key(x) ke hisaab se ascending sort hota hai.
# Highest marks pehle chahiye to key = -marks, lowest pehle ke liye key = marks.
# ---------------------------------------------------------------
def bubble_sort(arr, key):
    a, comps, swaps = arr[:], 0, 0
    n = len(a)
    for i in range(n):
        swapped = False
        for j in range(n - i - 1):
            comps += 1
            if key(a[j]) > key(a[j + 1]):
                a[j], a[j + 1] = a[j + 1], a[j]
                swaps += 1
                swapped = True
        if not swapped:  # list pehle se sorted ho to ruk jao
            break
    return a, comps, swaps


def selection_sort(arr, key):
    a, comps, swaps = arr[:], 0, 0
    n = len(a)
    for i in range(n - 1):
        smallest = i
        for j in range(i + 1, n):
            comps += 1
            if key(a[j]) < key(a[smallest]):
                smallest = j
        if smallest != i:
            a[i], a[smallest] = a[smallest], a[i]
            swaps += 1
    return a, comps, swaps


def insertion_sort(arr, key):
    a, comps, swaps = arr[:], 0, 0
    for i in range(1, len(a)):
        current = a[i]
        j = i - 1
        while j >= 0:
            comps += 1
            if key(a[j]) > key(current):
                a[j + 1] = a[j]  # element ko aage shift karo
                swaps += 1
                j -= 1
            else:
                break
        a[j + 1] = current
    return a, comps, swaps


def merge_sort(arr, key):
    stats = {"comparisons": 0, "moves": 0}

    def sort(lst):
        if len(lst) <= 1:
            return lst
        mid = len(lst) // 2
        left = sort(lst[:mid])
        right = sort(lst[mid:])
        return merge(left, right)

    def merge(left, right):
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            stats["comparisons"] += 1
            if key(left[i]) <= key(right[j]):
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
            stats["moves"] += 1
        rest = left[i:] + right[j:]
        stats["moves"] += len(rest)
        return result + rest

    return sort(arr[:]), stats["comparisons"], stats["moves"]


def quick_sort(arr, key):
    a, comps, swaps = arr[:], 0, 0
    stack = [(0, len(a) - 1)]  # recursion ki jagah stack (bare data par safe)
    while stack:
        low, high = stack.pop()
        if low >= high:
            continue
        p = random.randint(low, high)  # random pivot
        a[p], a[high] = a[high], a[p]
        pivot = key(a[high])
        i = low
        for j in range(low, high):
            comps += 1
            if key(a[j]) < pivot:
                a[i], a[j] = a[j], a[i]
                swaps += 1
                i += 1
        a[i], a[high] = a[high], a[i]
        swaps += 1
        stack.append((low, i - 1))
        stack.append((i + 1, high))
    return a, comps, swaps


ALGORITHMS = {
    "Bubble Sort": bubble_sort,
    "Insertion Sort": insertion_sort,
    "Selection Sort": selection_sort,
    "Merge Sort": merge_sort,
    "Quick Sort": quick_sort,
}

INFO = {
    "Bubble Sort": "Best O(n) | Average O(n²) | Worst O(n²) | Space O(1) | Stable",
    "Insertion Sort": "Best O(n) | Average O(n²) | Worst O(n²) | Space O(1) | Stable",
    "Selection Sort": "Best O(n²) | Average O(n²) | Worst O(n²) | Space O(1) | Not stable",
    "Merge Sort": "Best O(n log n) | Average O(n log n) | Worst O(n log n) | Space O(n) | Stable",
    "Quick Sort": "Best O(n log n) | Average O(n log n) | Worst O(n²) | Space O(log n) | Not stable",
}

HOW_IT_WORKS = {
    "Bubble Sort": "Compares neighbouring elements and swaps them if they are in the wrong order. "
                   "The biggest value 'bubbles' to the end in every pass.",
    "Insertion Sort": "Takes one element at a time and inserts it at the correct place in the already sorted part.",
    "Selection Sort": "Finds the best (smallest) element in the unsorted part and puts it at the front.",
    "Merge Sort": "Splits the list into halves, sorts each half and merges the two sorted halves.",
    "Quick Sort": "Picks a pivot, puts smaller elements on one side and bigger ones on the other, "
                  "then repeats for both sides.",
}


# ---------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------
def load_file(f):
    if f.name.lower().endswith((".xlsx", ".xls")):
        return pd.read_excel(f)
    return pd.read_csv(f)


def add_ranks(df):
    # Same marks wale students ko same rank (1, 2, 2, 4)
    ranks, prev, rank = [], None, 0
    for idx, m in enumerate(df["Marks"], start=1):
        if m != prev:
            rank = idx
            prev = m
        ranks.append(rank)
    df.insert(0, "Rank", ranks)
    return df


sample_csv = "Roll No,Name,Marks\n1,Ali Khan,85\n2,Sara Malik,92\n3,Usman Raza,70\n4,Hira Butt,92\n5,Bilal Ahmed,64\n"

# ---------------------------------------------------------------
# STEP 1: UPLOAD
# ---------------------------------------------------------------
st.markdown('<div class="step">Step 1: File upload </div>', unsafe_allow_html=True)
up_col, help_col = st.columns([3, 1])
with up_col:
    file = st.file_uploader("CSV OR Excel file (.csv, .xlsx)", type=["csv", "xlsx", "xls"],
                            label_visibility="collapsed")
with help_col:
    st.download_button("📄 Sample file download", sample_csv, file_name="sample_students.csv", mime="text/csv",
                       use_container_width=True)
    st.caption("To understand the format")

if file is None:
    st.info("👆 Upload the students file. The file must contain at least two columns: Name and Marks")
    with st.expander("📖 How do the sorting algorithms work?"):
        for algo, text in HOW_IT_WORKS.items():
            st.markdown(f"**{algo}**: {text}  \n`{INFO[algo]}`")
    st.stop()

try:
    raw = load_file(file)
except Exception as e:
    st.error(f"Cannot read the file : {e}")
    st.stop()

if raw.empty:
    st.error("File is empty")
    st.stop()

# ---------------------------------------------------------------
# STEP 2: SETTINGS
# ---------------------------------------------------------------
st.markdown('<div class="step">Step 2: Choose columns, algorithm and settings </div>', unsafe_allow_html=True)

cols = list(raw.columns)
guess_name = next((c for c in cols if "name" in str(c).lower()), cols[0])
guess_marks = next((c for c in cols if any(k in str(c).lower() for k in ["mark", "score", "total", "grade"])),
                   cols[-1])

s1, s2, s3, s4 = st.columns([1, 1, 1, 1])
name_col = s1.selectbox("Name column", cols, index=cols.index(guess_name))
marks_col = s2.selectbox("Marks column", cols, index=cols.index(guess_marks))
algo_name = s3.selectbox("Sorting Algorithm", list(ALGORITHMS.keys()), index=3)
order = s4.radio("Order", ["Highest marks first", "Lowest marks first"])
descending = order.startswith("Highest")

st.caption(f"**{algo_name}**: {HOW_IT_WORKS[algo_name]}  |  `{INFO[algo_name]}`")

df = raw.copy()
df["_marks"] = pd.to_numeric(df[marks_col], errors="coerce")
invalid = int(df["_marks"].isna().sum())
df = df.dropna(subset=["_marks"]).reset_index(drop=True)

if invalid:
    st.warning(f"{invalid} Rows with non-numeric marks will be ignored.")
if df.empty:
    st.error("No valid numbers were found in the Marks column. Please select the correct column.")
    st.stop()

if len(df) > 5000 and algo_name in ("Bubble Sort", "Insertion Sort", "Selection Sort"):
    st.warning(f"{algo_name} is O(n²), so it can be slow for {len(df):,} students. "
               f"Merge Sort or Quick Sort is recommended.")

top_n = st.slider("How many top students would you like to see?", 1, len(df), min(10, len(df)))

with st.expander(f"📋 Uploaded data preview ({len(raw)} rows)"):
    st.dataframe(raw, use_container_width=True, hide_index=True)

# ---------------------------------------------------------------
# STEP 3: SORT
# ---------------------------------------------------------------
st.markdown('<div class="step">Step 3: Sort </div>', unsafe_allow_html=True)

if st.button(f"🚀 Run {algo_name}", type="primary", use_container_width=True):
    records = df.to_dict("records")
    key = (lambda r: -r["_marks"]) if descending else (lambda r: r["_marks"])
    t0 = time.perf_counter()
    sorted_records, comparisons, swaps = ALGORITHMS[algo_name](records, key)
    elapsed = (time.perf_counter() - t0) * 1000
    st.session_state.result = {
        "df": pd.DataFrame(sorted_records),
        "algo": algo_name,
        "comparisons": comparisons,
        "swaps": swaps,
        "ms": elapsed,
        "name_col": name_col,
        "marks_col": marks_col,
        "top_n": top_n,
        "descending": descending,
    }

# ---------------------------------------------------------------
# RESULTS
# ---------------------------------------------------------------
res = st.session_state.get("result")
if res:
    out = res["df"].copy()
    out["Marks"] = out["_marks"]
    out = out.drop(columns=["_marks"])
    out = out.rename(columns={res["name_col"]: "Name"}) if res["name_col"] != "Name" else out
    if res["marks_col"] != "Marks" and res["marks_col"] in out.columns:
        out = out.drop(columns=[res["marks_col"]])
    other = [c for c in out.columns if c not in ("Name", "Marks")]
    out = out[["Name", "Marks"] + other]
    out = add_ranks(out)
    n = min(res["top_n"], len(out))
    top = out.head(n)

    st.divider()
    st.success(f"Sorted using **{res['algo']}**")
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Total Students", len(out))
    m2.metric("Average Marks", f"{out['Marks'].mean():.1f}")
    m3.metric("Comparisons", f"{res['comparisons']:,}")
    m4.metric("Swaps / Moves", f"{res['swaps']:,}")
    m5.metric("Sorting Time", f"{res['ms']:.3f} ms")

    tab1, tab2, tab3 = st.tabs(["🏅 Top Students", "📋 Complete List", "📊 Chart"])

    with tab1:
        if res["descending"] and len(top) >= 1:
            pod = st.columns(min(3, len(top)))
            styles = [("🥇", "gold"), ("🥈", "silver"), ("🥉", "bronze")]
            for i, c in enumerate(pod):
                row = top.iloc[i]
                medal, cls = styles[i]
                c.markdown(
                    f'<div class="podium {cls}"><div class="medal">{medal}</div>'
                    f'<div class="name">{row["Name"]}</div>'
                    f'<div class="marks">{row["Marks"]:g}</div></div>',
                    unsafe_allow_html=True,
                )
            st.write("")
        st.subheader(f"Top {n} Students")
        st.dataframe(top, use_container_width=True, hide_index=True)
        st.download_button("⬇️ Top students CSV download", top.to_csv(index=False), "top_students.csv",
                           "text/csv")

    with tab2:
        q = st.text_input("🔎 Search by name")
        view = out[out["Name"].astype(str).str.contains(q, case=False, na=False)] if q else out
        st.dataframe(view, use_container_width=True, hide_index=True)
        st.download_button("⬇️ Sorted list download", out.to_csv(index=False), "sorted_students.csv",
                           "text/csv")

    with tab3:
        st.bar_chart(top.set_index("Name")["Marks"])

st.caption("Sorting algorithms: Bubble | Insertion | Selection | Merge | Quick")