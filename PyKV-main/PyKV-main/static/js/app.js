let opsChart;
let cacheChart;

async function setKey() {
    const key = document.getElementById("key").value;
    const value = document.getElementById("value").value;

    if (!key) {
        showToast("Please enter a key", "error");
        return;
    }

    try {
        const res = await fetch("/set", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ key, value })
        });

        const data = await res.json();
        
        if (res.ok) {
            showToast("Key SET successfully ✅", "success");
            document.getElementById("key").value = "";
            document.getElementById("value").value = "";
        } else {
            showToast("Failed to SET key ❌", "error");
            console.error("SET error:", data);
        }
    } catch (error) {
        showToast("Error: " + error.message, "error");
        console.error("SET fetch error:", error);
    }
}

async function getKey() {
    const key = document.getElementById("key").value;

    if (!key) {
        showToast("Please enter a key", "error");
        return;
    }

    try {
        const res = await fetch(`/get/${key}`);

        if (res.ok) {
            const data = await res.json();
            document.getElementById("value").value = data.value;
            showToast("Key GET successfully ✅", "success");
        } else {
            showToast("Key not found ❌", "error");
        }
    } catch (error) {
        showToast("Error: " + error.message, "error");
        console.error("GET fetch error:", error);
    }
}

async function deleteKey() {
    const key = document.getElementById("key").value;

    if (!key) {
        showToast("Please enter a key", "error");
        return;
    }

    try {
        const res = await fetch(`/delete/${key}`, {
            method: "DELETE"
        });

        if (res.ok) {
            showToast("Key DELETE successfully ✅", "success");
            document.getElementById("key").value = "";
            document.getElementById("value").value = "";
        } else {
            showToast("Failed to DELETE key ❌", "error");
        }
    } catch (error) {
        showToast("Error: " + error.message, "error");
        console.error("DELETE fetch error:", error);
    }
}

function showToast(message, type = "success") {
    const toast = document.getElementById("toast");
    toast.innerText = message;
    toast.className = `toast show ${type}`;

    setTimeout(() => {
        toast.classList.remove("show");
    }, 3000);
}

async function logout() {
    showToast("Logged out successfully 👋", "success");
    setTimeout(() => {
        window.location.href = "/";
    }, 800);
}
async function loadStats() {
    const res = await fetch("/stats");
    const data = await res.json();

    document.getElementById("total_keys").innerText = data.total_keys;
    document.getElementById("capacity").innerText = data.capacity;
    document.getElementById("hits").innerText = data.hits;
    document.getElementById("misses").innerText = data.misses;
    document.getElementById("set_ops").innerText = data.set_ops;
    document.getElementById("get_ops").innerText = data.get_ops;
    document.getElementById("delete_ops").innerText = data.delete_ops;
    document.getElementById("total_hits").innerText = data.total_keys;
}


async function loadCharts() {
    const res = await fetch("/stats");
    const data = await res.json();

    // -------- OPERATIONS BAR CHART --------
    const opsCtx = document.getElementById("opsChart").getContext("2d");

    if (opsChart) opsChart.destroy();

    opsChart = new Chart(opsCtx, {
        type: "bar",
        data: {
            labels: ["SET", "GET", "DELETE"],
            datasets: [{
                label: "Operations Count",
                data: [data.set_ops, data.get_ops, data.delete_ops],
                backgroundColor: ["#3b82f6", "#10b981", "#ef4444"]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: false }
            }
        }
    });

    // -------- CACHE DOUGHNUT CHART --------
    const cacheCtx = document.getElementById("cacheChart").getContext("2d");

    if (cacheChart) cacheChart.destroy();

    cacheChart = new Chart(cacheCtx, {
        type: "doughnut",
        data: {
            labels: ["Hits", "Misses"],
            datasets: [{
                data: [data.hits, data.misses],
                backgroundColor: ["#10b981", "#f59e0b"]
            }]
        },
        options: {
            responsive: true
        }
    });
}

async function openStatModal(type) {
    const res = await fetch("/stats");
    const data = await res.json();

    let title = "";
    let content = "";

    switch (type) {
        case "total_keys":
            title = "Total Keys";
            content = `Total keys currently stored: ${data.total_keys}\n\nThis represents the number of active key-value pairs present in memory right now.`;
            break;
        case "capacity":
            title = "Cache Capacity";
            content = `Cache capacity: ${data.capacity}\n\nThis is the maximum number of keys the cache can hold. When exceeded, LRU eviction occurs.`;
            break;
        case "hits":
            title = "Cache Hits";
            content = `Cache hits: ${data.hits}\n\nNumber of successful GET operations where the key was found in memory.`;
            break;
        case "misses":
            title = "Cache Misses";
            content = `Cache misses: ${data.misses}\n\nNumber of GET operations where the key was NOT found.`;
            break;
        case "set_ops":
            title = "SET Operations";
            content = `Total SET operations: ${data.set_ops}\n\nCounts how many times new or existing keys were written.`;
            break;
        case "get_ops":
            title = "GET Operations";
            content = `Total GET operations: ${data.get_ops}\n\nCounts all read requests (hits + misses).`;
            break;
        case "delete_ops":
            title = "DELETE Operations";
            content = `Total DELETE operations: ${data.delete_ops}\n\nCounts how many keys were removed from the cache.`;
            break;
        case "all_data":
            title = "All Stored Data";
            try {
                const allDataRes = await fetch("/all-data");
                if (!allDataRes.ok) {
                    throw new Error(`HTTP error! status: ${allDataRes.status}`);
                }
                const allData = await allDataRes.json();
                console.log("All data response:", allData);
                
                if (!allData.data || allData.data.length === 0) {
                    content = "No data stored yet. Start by using the SET button to save key-value pairs.";
                    document.getElementById("modalTitle").innerText = title;
                    document.getElementById("modalContent").innerText = content;
                } else {
                    let tableHTML = `<p>${allData.count} key-value pair(s) stored</p>
                    <table>
                        <thead>
                            <tr>
                                <th>Key</th>
                                <th>Value</th>
                            </tr>
                        </thead>
                        <tbody>`;
                    
                    allData.data.forEach(item => {
                        const safeKey = item.key.replace(/</g, "&lt;").replace(/>/g, "&gt;");
                        const safeValue = item.value.replace(/</g, "&lt;").replace(/>/g, "&gt;");
                        tableHTML += `<tr>
                                <td>${safeKey}</td>
                                <td>${safeValue}</td>
                            </tr>`;
                    });
                    tableHTML += `</tbody></table>`;
                    
                    document.getElementById("modalTitle").innerText = title;
                    document.getElementById("modalContent").innerHTML = tableHTML;
                }
            } catch (err) {
                console.error("Error fetching data:", err);
                content = "Error loading data: " + err.message;
                document.getElementById("modalTitle").innerText = title;
                document.getElementById("modalContent").innerText = content;
            }
            document.getElementById("modalOverlay").classList.add("show");
            document.getElementById("statModal").classList.add("show");
            return;
    }

    document.getElementById("modalTitle").innerText = title;
    document.getElementById("modalContent").innerHTML = content;

    document.getElementById("modalOverlay").classList.add("show");
    document.getElementById("statModal").classList.add("show");
}

function closeModal() {
    document.getElementById("modalOverlay").classList.remove("show");
    document.getElementById("statModal").classList.remove("show");
}
