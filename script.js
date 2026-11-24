const chart = document.getElementById("chart");
const chartKicker = document.getElementById("chart-kicker");
const chartNumber = document.getElementById("chart-number");
const chartCaption = document.getElementById("chart-caption");
const steps = [...document.querySelectorAll(".step")];
const progressBar = document.getElementById("progress-bar");

const palette = {
  intro: "#557b91",
  introLight: "#aebfc7",
  extra: "#dc9a57",
  extraLight: "#edcba7",
  neither: "#89907d",
  ink: "#17191a",
  red: "#ad5b47"
};

function svgStart(viewBox = "0 0 700 500") {
  return `<svg viewBox="${viewBox}" aria-hidden="true" class="chart-enter">`;
}

function renderBalance() {
  chartKicker.textContent = "RESPONDENT BALANCE";
  chartNumber.textContent = "n = 2,900";
  chartCaption.textContent = "The classes are nearly balanced: 1,491 extroverts and 1,409 introverts.";
  chart.innerHTML = svgStart() + `
    <g transform="translate(60 70)">
      <text x="0" y="0" fill="${palette.ink}" font-size="11">SHARE OF RESPONSES</text>
      <rect x="0" y="58" width="580" height="104" rx="52" fill="${palette.introLight}"/>
      <rect x="0" y="58" width="298" height="104" rx="52" fill="${palette.extra}"/>
      <circle cx="298" cy="110" r="8" fill="${palette.ink}"/>
      <text x="48" y="118" fill="#fff" font-size="16">51.4%</text>
      <text x="380" y="118" fill="${palette.ink}" font-size="16">48.6%</text>
      <text x="0" y="205" fill="${palette.extra}" font-size="12">EXTROVERT</text>
      <text x="490" y="205" fill="${palette.intro}" font-size="12" text-anchor="end">INTROVERT</text>
      <g transform="translate(0 280)">
        <line x1="0" y1="0" x2="580" y2="0" stroke="${palette.ink}" stroke-opacity=".18"/>
        <text x="290" y="42" text-anchor="middle" fill="${palette.ink}" font-size="11">NEARLY EVENLY SPLIT — IDEAL FOR COMPARISON</text>
      </g>
    </g>
  </svg>`;
}

function renderTime() {
  chartKicker.textContent = "MEAN / REPORTED SCALE";
  chartNumber.textContent = "5 BEHAVIOR VARIABLES";
  chartCaption.textContent = "Group means; each row is scaled to its own observed range. Values are labeled beside the bars.";
  const groups = [
    ["Time alone", 7.08, 2.07, 11],
    ["Social events", 1.78, 6.02, 10],
    ["Go outside", 1.27, 4.63, 7],
    ["Friend circle", 3.20, 9.17, 15],
    ["Post frequency", 1.37, 5.64, 10]
  ];
  let rows = "";
  groups.forEach((g, i) => {
    const y = 95 + i * 64;
    const introW = g[1] / g[3] * 250;
    const extraW = g[2] / g[3] * 250;
    rows += `
      <text x="0" y="${y - 30}" fill="${palette.ink}" font-size="11">${g[0].toUpperCase()}</text>
      <rect x="0" y="${y - 20}" width="${extraW}" height="18" rx="9" fill="${palette.extra}"/>
      <rect x="260" y="${y - 20}" width="${introW}" height="18" rx="9" fill="${palette.intro}"/>
      <text x="${extraW + 8}" y="${y - 7}" fill="${palette.ink}" font-size="10">${g[2].toFixed(1)}</text>
      <text x="${268 + introW}" y="${y - 7}" fill="${palette.ink}" font-size="10">${g[1].toFixed(1)}</text>
    `;
  });
  chart.innerHTML = svgStart() + `
    <g transform="translate(70 42)">
      <text x="0" y="0" fill="${palette.extra}" font-size="10">EXTROVERT</text>
      <text x="260" y="0" fill="${palette.intro}" font-size="10">INTROVERT</text>
      ${rows}
      <g transform="translate(0 430)">
        <line x1="0" y1="0" x2="510" y2="0" stroke="${palette.ink}" stroke-opacity=".18"/>
        <text x="255" y="28" text-anchor="middle" fill="${palette.ink}" font-size="10">MEAN RESPONSE — ORIGINAL SURVEY SCALE</text>
      </g>
    </g>
  </svg>`;
}

function renderCost() {
  chartKicker.textContent = "PERCENT ANSWERING YES";
  chartNumber.textContent = "TWO SOCIAL CUES";
  chartCaption.textContent = "Stage fear: 92.2% of introverts vs. 7.4% of extroverts. Feeling drained: 92.0% vs. 7.4%.";
  chart.innerHTML = svgStart() + `
    <g transform="translate(70 40)">
      ${[
        ["STAGE FEAR", 92.2, 7.4],
        ["DRAINED AFTER SOCIALIZING", 92.0, 7.4]
      ].map((g, i) => {
        const y = i * 180;
        return `
          <text x="0" y="${y}" fill="${palette.ink}" font-size="11">${g[0]}</text>
          <rect x="0" y="${y + 28}" width="520" height="42" rx="21" fill="${palette.extraLight}"/>
          <rect x="0" y="${y + 28}" width="${520 * g[2] / 100}" height="42" rx="21" fill="${palette.extra}"/>
          <text x="${520 * g[2] / 100 + 12}" y="${y + 56}" fill="${palette.ink}" font-size="13">${g[2]}% ext.</text>
          <rect x="0" y="${y + 82}" width="520" height="42" rx="21" fill="${palette.introLight}"/>
          <rect x="0" y="${y + 82}" width="${520 * g[1] / 100}" height="42" rx="21" fill="${palette.intro}"/>
          <text x="${520 * g[1] / 100 - 74}" y="${y + 110}" fill="#fff" font-size="13">${g[1]}% intro.</text>
        `;
      }).join("")}
      <g transform="translate(0 390)">
        <text x="0" y="0" fill="${palette.ink}" font-size="10">CATEGORICAL SURVEY SIGNAL</text>
        <line x1="0" y1="28" x2="520" y2="28" stroke="${palette.ink}" stroke-opacity=".18"/>
      </g>
    </g>
  </svg>`;
}

function renderContinuum() {
  chartKicker.textContent = "MIES SELF-LABEL × CONTINUOUS SCORE";
  chartNumber.textContent = "n = 7,163 LABELED";
  chartCaption.textContent = "7,163 mapped labels from 7,188 records. Mean ±1 standard deviation on 8 shared items, keyed 1–5.";
  const groups = [
    ["Introvert", 2.175, palette.intro, 0.772],
    ["Neither", 3.134, palette.neither, 0.843],
    ["Extrovert", 4.078, palette.extra, 0.700]
  ];
  let dots = "";
  groups.forEach((g, i) => {
    const cy = 145 + i * 105;
    const scoreX = score => 170 + (score - 1) * 112;
    const low = scoreX(Math.max(1, g[1] - g[3]));
    const high = scoreX(Math.min(5, g[1] + g[3]));
    const mean = scoreX(g[1]);
    dots += `
      <text x="0" y="${cy + 4}" fill="${palette.ink}" font-size="10">${g[0].toUpperCase()}</text>
      <line x1="${low}" y1="${cy}" x2="${high}" y2="${cy}" stroke="${g[2]}" stroke-width="4" stroke-linecap="round"/>
      <line x1="${low}" y1="${cy - 9}" x2="${low}" y2="${cy + 9}" stroke="${g[2]}" stroke-width="2"/>
      <line x1="${high}" y1="${cy - 9}" x2="${high}" y2="${cy + 9}" stroke="${g[2]}" stroke-width="2"/>
      <circle cx="${mean}" cy="${cy}" r="8" fill="${g[2]}" stroke="#f4f1ea" stroke-width="3"/>
      <text x="${mean}" y="${cy - 15}" text-anchor="middle" fill="${palette.ink}" font-size="10">${g[1].toFixed(2)}</text>
    `;
  });
  const ticks = [1, 2, 3, 4, 5].map(score => {
    const x = 170 + (score - 1) * 112;
    return `<line x1="${x}" y1="105" x2="${x}" y2="380" stroke="${palette.ink}" stroke-opacity=".1"/>
      <text x="${x}" y="405" text-anchor="middle" fill="${palette.ink}" font-size="10">${score}</text>`;
  }).join("");
  chart.innerHTML = svgStart() + `
    <g transform="translate(30 20)">
      <text x="0" y="10" fill="${palette.ink}" font-size="10">SELF-IDENTIFICATION</text>
      <text x="170" y="10" fill="${palette.ink}" font-size="10">ITEM SCORE (1–5)</text>
      ${ticks}
      ${dots}
      <text x="170" y="445" fill="${palette.ink}" font-size="9">LESS EXTROVERTED</text>
      <text x="618" y="445" text-anchor="end" fill="${palette.ink}" font-size="9">MORE EXTROVERTED</text>
    </g>
  </svg>`;
}

function renderContext() {
  chartKicker.textContent = "DATASET MAP";
  chartNumber.textContent = "SEPARATE SOURCES";
  chartCaption.textContent = "Different instruments and samples. No respondent IDs connect these sources.";
  chart.innerHTML = svgStart() + `
    <g transform="translate(80 50)">
      <circle cx="270" cy="210" r="155" fill="none" stroke="${palette.ink}" stroke-opacity=".16"/>
      <circle cx="270" cy="210" r="72" fill="${palette.ink}" fill-opacity=".06" stroke="${palette.ink}" stroke-opacity=".28"/>
      ${[
        [70, 100, "BEHAVIOR", "7 behaviors", palette.extra],
        [470, 100, "BIG5", "50 items", palette.extraLight],
        [70, 330, "IPIP", "50 items", palette.intro],
        [470, 330, "MIES", "91 items", palette.neither]
      ].map(d => `
        <circle cx="${d[0]}" cy="${d[1]}" r="54" fill="${d[4]}" fill-opacity=".92"/>
        <text x="${d[0]}" y="${d[1] - 4}" text-anchor="middle" fill="${d[4] === palette.extraLight ? palette.ink : "#fff"}" font-size="11">${d[2]}</text>
        <text x="${d[0]}" y="${d[1] + 18}" text-anchor="middle" fill="${d[4] === palette.extraLight ? palette.ink : "#fff"}" font-size="14">${d[3]}</text>
      `).join("")}
      <text x="270" y="205" text-anchor="middle" fill="${palette.ink}" font-size="12">NO COMMON</text>
      <text x="270" y="224" text-anchor="middle" fill="${palette.ink}" font-size="12">RESPONDENT IDS</text>
    </g>
  </svg>`;
}

const renderers = [renderBalance, renderTime, renderCost, renderContinuum, renderContext];

const observer = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (!entry.isIntersecting) return;
    steps.forEach(step => step.classList.remove("active"));
    entry.target.classList.add("active");
    const index = Number(entry.target.dataset.step);
    renderers[index]();
  });
}, { threshold: 0.58 });

steps.forEach(step => observer.observe(step));

function updateProgress() {
  const max = document.documentElement.scrollHeight - window.innerHeight;
  const ratio = max > 0 ? window.scrollY / max : 0;
  progressBar.style.width = `${Math.max(0, Math.min(1, ratio)) * 100}%`;
}
window.addEventListener("scroll", updateProgress, { passive: true });
updateProgress();
renderBalance();

const dialog = document.getElementById("data-dialog");
document.getElementById("top-note").addEventListener("click", () => dialog.showModal());
document.getElementById("dialog-close").addEventListener("click", () => dialog.close());
dialog.addEventListener("click", event => {
  if (event.target === dialog) dialog.close();
});
document.getElementById("return-button").addEventListener("click", () => {
  document.getElementById("intro").scrollIntoView({ behavior: "smooth" });
});
