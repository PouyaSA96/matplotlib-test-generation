const puppeteer = require('puppeteer');
const URLS = [
    'https://matplotlib.org/stable/gallery/lines_bars_and_markers/simple_plot.html',
    'https://matplotlib.org/stable/gallery/lines_bars_and_markers/bar_stacked.html',
    'https://matplotlib.org/stable/gallery/lines_bars_and_markers/bar_label_demo.html',
    'https://matplotlib.org/stable/gallery/lines_bars_and_markers/stackplot_demo.html',
    'https://matplotlib.org/stable/gallery/lines_bars_and_markers/eventplot_demo.html',
    'https://matplotlib.org/stable/gallery/lines_bars_and_markers/marker_reference.html',
    'https://matplotlib.org/stable/gallery/lines_bars_and_markers/linestyles.html',
    'https://matplotlib.org/stable/gallery/lines_bars_and_markers/scatter_hist.html',
    'https://matplotlib.org/stable/gallery/statistics/errorbar_features.html',
    'https://matplotlib.org/stable/gallery/statistics/histogram_histogram2d.html',
    'https://matplotlib.org/stable/gallery/statistics/boxplot_demo.html',
    'https://matplotlib.org/stable/gallery/statistics/violinplot.html',
    'https://matplotlib.org/stable/gallery/images_contours_and_fields/contour_demo.html',
    'https://matplotlib.org/stable/gallery/images_contours_and_fields/contourf_demo.html',
    'https://matplotlib.org/stable/gallery/images_contours_and_fields/image_demo.html',
    'https://matplotlib.org/stable/gallery/images_contours_and_fields/irradiance.html',
    'https://matplotlib.org/stable/gallery/text_labels_and_annotations/annotation_demo.html',
    'https://matplotlib.org/stable/gallery/text_labels_and_annotations/text_intro.html',
    'https://matplotlib.org/stable/gallery/color/colormap_reference.html',
    'https://matplotlib.org/stable/gallery/color/colormaps_reference.html',
    'https://matplotlib.org/stable/gallery/subplots_axes_and_figures/subplots_demo.html',
    'https://matplotlib.org/stable/gallery/subplots_axes_and_figures/shared_axis_demo.html'
   ];
const VIEWPORTS = [
  { width:800, height:600 },
  { width:1200, height:800 },
  { width:400, height:300 },
  { width:1024, height:768 },
];
const TESTS = [];
for (const url of URLS) {
  for (const vp of VIEWPORTS) {
    TESTS.push({ url, vp });
  }
} 

describe("Gallery smoke", () => {
  let browser;
  beforeAll(async () => browser = await puppeteer.launch());
  afterAll(async () => browser.close());

  for (const t of TESTS) {
    test(`${t.url} @${t.vp.width}x${t.vp.height}`, async () => {
      const page = await browser.newPage();
      await page.setViewport(t.vp);
      const res = await page.goto(t.url);
      expect(res.status()).toBe(200);
      expect(await page.$('img[src*="/_images/"]')).not.toBeNull();
    }, 15_000);
  }
});
