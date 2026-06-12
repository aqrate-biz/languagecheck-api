# Status

<div style="display:grid;gap:0.75rem;max-width:900px;">
	<!--<div style="display:flex;gap:0.5rem;flex-wrap:wrap;align-items:center;">
		<button id="check-status-btn" type="button" style="padding:0.55rem 0.9rem;border:1px solid #0b57d0;background:#0b57d0;color:#fff;border-radius:8px;cursor:pointer;">Check status</button>
		<button id="clear-status-btn" type="button" style="padding:0.55rem 0.9rem;border:1px solid #d0d7de;background:#fff;color:#24292f;border-radius:8px;cursor:pointer;">Clear</button>
		<span id="status-pill" style="padding:0.3rem 0.6rem;border-radius:999px;border:1px solid #d0d7de;font-size:0.85rem;">Idle</span>
	</div>-->

    <!--<div>
    	<strong>Request</strong>
    	<pre style="margin-top:0.35rem;">GET /v2/status</pre>
    </div>-->

    <!--<div>
    	<strong>Response</strong>
    	<pre id="status-output" style="margin-top:0.35rem;padding:0.9rem;border-radius:8px;background:#0f172a;color:#e2e8f0;overflow:auto;max-height:420px;">No request sent yet.</pre>
    </div>-->

    <div id="status-history" style="display:grid;gap:0.6rem;margin-top:0.6rem;">
        <div>
            <strong>Recent API status history</strong>
            <p id="status-history-loading" style="margin:0.35rem 0 0;color:#4b5563;">Loading recent status history...</p>
        </div>
        <div id="status-history-grid" style="display:flex;flex-wrap:wrap;gap:3px;align-content:flex-start;"></div>
    	<hr>
        <div style="display:flex;flex-wrap:wrap;gap:0.9rem;font-size:0.9rem;color:#4b5563;">
            <span style="display:flex;align-items:center;gap:0.35rem;"><span style="width:10px;height:10px;border-radius:2px;background:#16a34a;border:1px solid rgba(15,23,42,0.15);"></span> all operational</span>
            <span style="display:flex;align-items:center;gap:0.35rem;"><span style="width:10px;height:10px;border-radius:2px;background:#facc15;border:1px solid rgba(15,23,42,0.15);"></span> mixed results</span>
            <span style="display:flex;align-items:center;gap:0.35rem;"><span style="width:10px;height:10px;border-radius:2px;background:#dc2626;border:1px solid rgba(15,23,42,0.15);"></span> degraded</span>
        </div>
    </div>

</div>

<script>
(() => {
	const API_URL = "https://apitest.languagecheck.it/v2/status";
	const checkBtn = document.getElementById("check-status-btn");
	const clearBtn = document.getElementById("clear-status-btn");
	const output = document.getElementById("status-output");
	const pill = document.getElementById("status-pill");
	const historyLoading = document.getElementById("status-history-loading");
	const historyGrid = document.getElementById("status-history-grid");
	const FIRESTORE_COLLECTION = "apiStatus";
	const MAX_ITEMS = 1000;

	function setPill(text, fg, bg, border) {
		pill.textContent = text;
		pill.style.color = fg;
		pill.style.background = bg;
		pill.style.borderColor = border;
	}

	function printJson(payload) {
		output.textContent = JSON.stringify(payload, null, 2);
	}

	function normalizeStatusValue(value) {
		return typeof value === "string" ? value.trim().toLowerCase() : "";
	}

	function normalizeTimestamp(value) {
		if (!value) {
			return null;
		}
		if (typeof value.toDate === "function") {
			return value.toDate();
		}
		if (value.seconds) {
			return new Date(value.seconds * 1000);
		}
		if (value instanceof Date) {
			return value;
		}
		if (typeof value === "string") {
			const parsed = Date.parse(value);
			return Number.isNaN(parsed) ? null : new Date(parsed);
		}
		return null;
	}

	function getHourBucket(timestamp) {
		const date = new Date(timestamp);
		return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, "0")}-${String(date.getDate()).padStart(2, "0")} ${String(date.getHours()).padStart(2, "0")}:00`;
	}

	function getBucketStatus(items) {
		const allOperational = items.every((item) => normalizeStatusValue(item.ai) === "operational" && normalizeStatusValue(item.system) === "operational");
		const hasOnlyIssues = items.every((item) => normalizeStatusValue(item.ai) !== "operational" || normalizeStatusValue(item.system) !== "operational");

		if (allOperational) {
			return { label: "All operational", color: "#16a34a" };
		}
		if (hasOnlyIssues) {
			return { label: "Degraded", color: "#dc2626" };
		}
		return { label: "Mixed results", color: "#facc15" };
	}

	function renderHistory(buckets) {
		historyGrid.innerHTML = "";
		historyLoading.textContent = "";
		if (!buckets.length) {
			historyLoading.textContent = "No status history available yet.";
			return;
		}

		const formatter = new Intl.DateTimeFormat(undefined, {
			year: "numeric",
			month: "short",
			day: "2-digit",
			hour: "2-digit",
			minute: "2-digit"
		});

		buckets.forEach((bucket) => {
			const square = document.createElement("div");
			square.style.width = "8px";
			square.style.height = "8px";
			square.style.borderRadius = "2px";
			square.style.border = "1px solid rgba(15, 23, 42, 0.15)";
			square.style.background = bucket.status.color;
			square.title = `${formatter.format(bucket.timestamp)} • ${bucket.status.label}`;
			historyGrid.appendChild(square);
		});
	}

	function loadFirebaseSdk() {
		return new Promise((resolve, reject) => {
			if (window.firebase && window.firebase.firestore) {
				resolve();
				return;
			}

			const appScript = document.createElement("script");
			appScript.src = "https://www.gstatic.com/firebasejs/10.12.2/firebase-app-compat.js";
			appScript.onload = () => {
				const firestoreScript = document.createElement("script");
				firestoreScript.src = "https://www.gstatic.com/firebasejs/10.12.2/firebase-firestore-compat.js";
				firestoreScript.onload = () => {
					if (window.firebase && window.firebase.firestore) {
						resolve();
					} else {
						reject(new Error("Firebase Firestore SDK is not available."));
					}
				};
				firestoreScript.onerror = () => {
					reject(new Error("Unable to load Firestore SDK."));
				};
				document.head.appendChild(firestoreScript);
			};
			appScript.onerror = () => {
				reject(new Error("Unable to load Firebase app SDK."));
			};
			document.head.appendChild(appScript);
		});
	}

	function loadHistory() {
		historyLoading.textContent = "Loading recent status history...";
		loadFirebaseSdk()
			.then(loadHistoryFromFirestore)
			.catch((error) => {
				console.error(error);
				historyLoading.textContent = error.message;
			});
	}

	function loadHistoryFromFirestore() {
		if (!window.firebase || !window.firebase.firestore) {
			historyLoading.textContent = "Firebase Firestore SDK is not available.";
			return;
		}

		const firebaseConfig = window.LANGUAGECHECK_FIREBASE_CONFIG || window.LANGUAGECHECK_FIREBASE_CONFIG_OVERRIDES || {};
		if (!firebaseConfig.projectId) {
			historyLoading.textContent = "Firebase project configuration is not available.";
			return;
		}

		if (!firebase.apps.length) {
			firebase.initializeApp(firebaseConfig);
		}

		const db = firebase.firestore();
		db.collection(FIRESTORE_COLLECTION)
			.orderBy("timestamp", "desc")
			.limit(MAX_ITEMS)
			.get()
			.then((snapshot) => {
				const groups = new Map();
				snapshot.forEach((doc) => {
					const data = doc.data();
					const timestamp = normalizeTimestamp(data.timestamp);
					if (!timestamp) {
						return;
					}

					const hourKey = getHourBucket(timestamp);
					if (!groups.has(hourKey)) {
						groups.set(hourKey, {
							hourKey,
							timestamp,
							items: []
						});
					}
					groups.get(hourKey).items.push(data);
				});

				const buckets = Array.from(groups.values())
					.map((bucket) => ({
						...bucket,
						status: getBucketStatus(bucket.items)
					}))
					.sort((left, right) => left.timestamp - right.timestamp);

				renderHistory(buckets);
			})
			.catch((error) => {
				console.error(error);
				historyLoading.textContent = "Unable to load status history from Firestore.";
			});
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

	//checkBtn.addEventListener("click", checkStatus);
	//clearBtn.addEventListener("click", clearView);
	loadHistory();
})();
</script>
