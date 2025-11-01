#include <iostream>
#include <vector>
#include <string>
#include <utility>

using namespace std;

// Edge u–v with saving w (exists: destroy; missing: build)
struct Edge { int u, v, w; }; 

// A-Z: 0..25; a-z: 26..51
int letterCost(char c) {
    if (c >= 'A' && c <= 'Z') return c - 'A';
    return (c - 'a') + 26;
}

// Split "010,101,110" into {"010","101","110"}
vector<string> splitRows(const string& s) {
    vector<string> rows; rows.reserve(64);
    string cur;
    for (int i = 0; i < (int)s.size(); ++i) {
        char ch = s[i];
        if (ch == ',') { 
            rows.push_back(cur); cur.clear(); 
        }
        else { cur.push_back(ch); }
    }
    rows.push_back(cur);
    return rows;
}

/// Build edges for i<j only. Also compute baseline destroy-all cost.
long long buildEdges(const vector<string>& country,
                     const vector<string>& build,
                     const vector<string>& destroy,
                     vector<Edge>& edges)
{
    int n = (int)country.size();
    long long baseDestroy = 0;

    for (int i = 0; i < n; ++i) {
        for (int j = i + 1; j < n; ++j) {
            bool exists = (country[i][j] == '1');

            int buildCost   = letterCost(build[i][j]);
            int destroyCost = letterCost(destroy[i][j]);

            if (exists) {
                baseDestroy += destroyCost;
            }

            Edge e;
            e.u = i;
            e.v = j;

            // saving w:
            // exists: destroyCost
            // missing: -buildCost
            if (exists) {
                e.w = destroyCost;
            } else {
                e.w = -buildCost;
            }

            edges.push_back(e);
        }
    }

    return baseDestroy;
}

// Selection sort by saving (w) in descending order.
void sortBySavingDesc(vector<Edge>& edges) {
    int m = (int)edges.size();
    for (int i = 0; i < m; ++i) {
        int best = i;
        for (int j = i + 1; j < m; ++j) {
            if (edges[j].w > edges[best].w) {
                best = j;
            }
        }
        if (best != i) {
            Edge tmp   = edges[i];
            edges[i]   = edges[best];
            edges[best]= tmp;
        }
    }
}

// Kruskal using simple component labels (no ranks, no path compression).
// total = sum of w for the chosen n-1 edges.
long long kruskalMaxSaving(int n, const vector<Edge>& edges) {
    vector<int> comp(n);
    for (int i = 0; i < n; ++i) {
        comp[i] = i;
    }

    long long total = 0;
    int used = 0;

    for (int i = 0; i < (int)edges.size() && used < n - 1; ++i) {
        int u = edges[i].u;
        int v = edges[i].v;
        int w = edges[i].w;

        if (comp[u] != comp[v]) {
            total += w;
            used += 1;

            int from = comp[v];
            int to   = comp[u];

            // merge: relabel all nodes with label "from" to label "to"
            for (int t = 0; t < n; ++t) {
                if (comp[t] == from) {
                    comp[t] = to;
                }
            }
        }
    }

    return total;
}

// Solve one case: parse, build edges and baseline, sort by saving, run Kruskal, return baseline minus total saving.
long long solveOne(const string& countryStr,
                   const string& buildStr,
                   const string& destroyStr)
{
    vector<string> country = splitRows(countryStr);
    vector<string> build   = splitRows(buildStr);
    vector<string> destroy = splitRows(destroyStr);
    int n = (int)country.size();

    vector<Edge> edges;
    edges.reserve(n * (n - 1) / 2);
    long long baseDestroy = buildEdges(country, build, destroy, edges);

    sortBySavingDesc(edges);
    long long totalSaving = kruskalMaxSaving(n, edges);

    return baseDestroy - totalSaving;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    // Read input, solve, print result.
    string countryStr, buildStr, destroyStr;
    if (!(cin >> countryStr >> buildStr >> destroyStr)) return 0;

    cout << solveOne(countryStr, buildStr, destroyStr) << "\n";
    return 0;
}