from tools_external import search_external, summarize_external_results

#results = search_external("login issues password reset")
results = search_external("problems with payment")

print("\n--- results ---")
for r in results:
    print(r["title"], "-", r["url"])

print("\n--- summary ---")
print(summarize_external_results(results))