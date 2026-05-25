# Status

This page performs a live request to the Status endpoint and shows the latest API response.

<div style="display:grid;gap:0.75rem;max-width:900px;">
	<div style="display:flex;gap:0.5rem;flex-wrap:wrap;align-items:center;">
		<button id="check-status-btn" type="button" style="padding:0.55rem 0.9rem;border:1px solid #0b57d0;background:#0b57d0;color:#fff;border-radius:8px;cursor:pointer;">Check status</button>
		<button id="clear-status-btn" type="button" style="padding:0.55rem 0.9rem;border:1px solid #d0d7de;background:#fff;color:#24292f;border-radius:8px;cursor:pointer;">Clear</button>
		<span id="status-pill" style="padding:0.3rem 0.6rem;border-radius:999px;border:1px solid #d0d7de;font-size:0.85rem;">Idle</span>
	</div>

    <div>
    	<strong>Request</strong>
    	<pre style="margin-top:0.35rem;">GET /v2/status</pre>
    </div>

    <div>
    	<strong>Response</strong>
    	<pre id="status-output" style="margin-top:0.35rem;padding:0.9rem;border-radius:8px;background:#0f172a;color:#e2e8f0;overflow:auto;max-height:420px;">No request sent yet.</pre>
    </div>

</div>

<script>
(() => {
	const API_URL = "https://apitest.languagecheck.it/v2/status";
	const checkBtn = document.getElementById("check-status-btn");
	const clearBtn = document.getElementById("clear-status-btn");
	const output = document.getElementById("status-output");
	const pill = document.getElementById("status-pill");

	function setPill(text, fg, bg, border) {
		pill.textContent = text;
		pill.style.color = fg;
		pill.style.background = bg;
		pill.style.borderColor = border;
	}

	function printJson(payload) {
		output.textContent = JSON.stringify(payload, null, 2);
	}

	async function checkStatus() {
		setPill("Loading", "#1f2937", "#f3f4f6", "#d1d5db");
		output.textContent = "Calling /v2/status...";
		checkBtn.disabled = true;

		try {
			const response = await fetch(API_URL, {
				method: "GET",
				headers: {
					"Accept": "application/json"
				}
			});

			const rawBody = await response.text();
			let body;
			try {
				body = rawBody ? JSON.parse(rawBody) : null;
			} catch {
				body = { raw: rawBody };
			}

			printJson({
				endpoint: "/v2/status",
				status: response.status,
				ok: response.ok,
				body
			});

			if (response.ok) {
				setPill("OK " + response.status, "#0f5132", "#d1e7dd", "#badbcc");
			} else {
				setPill("Error " + response.status, "#842029", "#f8d7da", "#f5c2c7");
			}
		} catch (error) {
			printJson({
				endpoint: "/v2/status",
				networkError: String(error)
			});
			setPill("Network error", "#842029", "#f8d7da", "#f5c2c7");
		} finally {
			checkBtn.disabled = false;
		}
	}

	function clearView() {
		output.textContent = "No request sent yet.";
		setPill("Idle", "", "", "#d0d7de");
	}

	checkBtn.addEventListener("click", checkStatus);
	clearBtn.addEventListener("click", clearView);
})();
</script>
