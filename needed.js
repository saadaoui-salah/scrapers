(async () => {
  const CHUNK_SIZE = 200; // 20 concurrent requests
  const GROUP_SIZE = 10000; // Responses per JSON file

  const secondId = "5C8LMqZ9dbQ3RWoe5pFk5fJPhgiBQtBYdMnzekfJpump";
  const query =
    "?device_id=1e5238d2-1364-47a7-a7d4-5ee3fa6d0679&client_id=gmgn_web_20250620-236-cb253e6&from_app=gmgn&app_ver=20250620-236-cb253e6&tz_name=Africa%2FAlgiers&tz_offset=3600&app_lang=en-US&fp_did=6860f6a3ab98d788cd942fe343a1d7c1&os=web";
  const baseUrl = "https://gmgn.ai/api/v1/wallet_token_info/sol/";

  let batchResults = [];
  let fileCounter = 1;

  // Helper to split array into chunks
  function chunk(array, size) {
    return Array.from({ length: Math.ceil(array.length / size) }, (_, i) =>
      array.slice(i * size, i * size + size)
    );
  }

  // Process in chunks of 20 concurrently
  for (const chunkGroup of chunk(wallets, CHUNK_SIZE)) {
    const results = await Promise.all(
      chunkGroup.map(async (wallet) => {
        const url = `${baseUrl}${wallet}/${secondId}${query}`;
        try {
          const res = await fetch(url, {
            method: "GET",
            headers: {
              Accept: "application/json",
            },
          });
          if (!res.ok) throw new Error(`HTTP ${res.status}`);
          const data = await res.json();
          return { wallet, data };
        } catch (e) {
          console.warn(`Failed ${wallet}`, e);
          return { wallet, error: e.toString() };
        }
      })
    );

    batchResults.push(...results);

    // When reaching 10,000 results, save to JSON file
    if (batchResults.length >= GROUP_SIZE) {
      const blob = new Blob([JSON.stringify(batchResults, null, 2)], {
        type: "application/json",
      });
      const a = document.createElement("a");
      a.href = URL.createObjectURL(blob);
      a.download = `wallets_batch_${fileCounter}.json`;
      a.click();
      fileCounter++;
      batchResults = [];
    }

    // Small delay to avoid flooding
    await new Promise((r) => setTimeout(r, 100));
  }

  // Download remaining results
  if (batchResults.length > 0) {
    const blob = new Blob([JSON.stringify(batchResults, null, 2)], {
      type: "application/json",
    });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = `wallets_batch_${fileCounter}.json`;
    a.click();
  }

  console.log("✅ All requests finished and saved.");
})();

(async () => {
  const baseUrl =
    "https://gmgn.ai/vas/api/v1/token_trades/sol/5C8LMqZ9dbQ3RWoe5pFk5fJPhgiBQtBYdMnzekfJpump";
  const baseParams = new URLSearchParams({
    device_id: "1e5238d2-1364-47a7-a7d4-5ee3fa6d0679",
    client_id: "gmgn_web_20250618-117-96551a0",
    from_app: "gmgn",
    app_ver: "20250618-117-96551a0",
    tz_name: "Africa/Algiers",
    tz_offset: "3600",
    app_lang: "en-US",
    fp_did: "6860f6a3ab98d788cd942fe343a1d7c1",
    os: "web",
    limit: "50",
    maker: "",
    from: "1749528000",
    to: "1749572100",
  });

  let cursor = null;
  let page = 1;
  let batch = 1;
  let batchResults = [];

  const fetchPage = async (url) => {
    try {
      const res = await fetch(url, {
        headers: {
          accept: "application/json, text/plain, */*",
        },
      });

      if (res.status === 401) {
        throw new Error(
          "❌ Unauthorized (401) – You may need updated cookies, headers, or tokens."
        );
      }

      if (!res.ok) {
        throw new Error(`❌ Request failed: ${res.status} ${res.statusText}`);
      }

      return await res.json();
    } catch (err) {
      console.error(err.message);
      return null;
    }
  };

  const saveBatch = (data, batchNum) => {
    const blob = new Blob([JSON.stringify(data, null, 2)], {
      type: "application/json",
    });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = `gmgn_trades_batch_${batchNum}.json`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  while (true) {
    let url = `${baseUrl}?${baseParams.toString()}`;
    if (cursor) url += `&cursor=${encodeURIComponent(cursor)}`;

    console.log(`📦 [Batch ${batch}] Fetching page ${page}...`);
    const json = await fetchPage(url);
    if (!json) break;

    const results = json?.data?.history;
    cursor = json?.data?.next;

    if (Array.isArray(results) && results.length > 0) {
      batchResults.push(...results);
    } else {
      console.log("🟡 No results returned on this page.");
      break;
    }

    // Save every 1000 pages as a new batch
    if (page % 1000 === 0) {
      console.log(
        `💾 Saving batch ${batch} with ${batchResults.length} records...`
      );
      saveBatch(batchResults, batch);
      batchResults = [];
      batch++;
    }

    if (!cursor) {
      console.log("✅ No more cursor found. All pages fetched.");
      break;
    }

    page++;
  }

  // Save remaining results if any
  if (batchResults.length > 0) {
    console.log(
      `💾 Saving final batch ${batch} with ${batchResults.length} records...`
    );
    saveBatch(batchResults, batch);
  }

  console.log("✅ All done.");
})();
