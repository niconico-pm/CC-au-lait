<!-- content from here -->
<link rel="stylesheet" href="/css/table.css">
<script type="text/javascript" src="/js/jquery-latest.js"></script>
<script type="text/javascript" src="/js/jquery.tablesorter.js"></script>
<script type="text/javascript" src="/js/sort.js"></script>
<h3>${name}のスコアデータ</h3>
<div style="height: 22px">${link}</div>
<div style="height: 22px"><div style="float: right">更新日:${date}</div></div>
<h3>総合データ</h3>
<table id="total" class="tablesorter">
<colgroup><col><col></colgroup>
<colgroup class="light"><col></colgroup>
<colgroup class="medium"><col></colgroup>
<colgroup class="beast"><col></colgroup>
<colgroup><col><colgroup>
<thead>
<tr>
  <th colspan="2"></th>
  <th>Light</th>
  <th>Medium</th>
  <th>Beast</th>
  <th>Total</th>
</tr>
</thead>
<tbody>
${totaltable}
</tbody>
</table>
<h3>スコアデータ</h3>
<table id="score" class="tablesorter">
<!-- 曲名 -->
<colgroup><col class="music-title"></colgroup>
<!-- Light -->
<colgroup class="light"><col class="score"><col class="medal"><col class="grade"><col class="level"></colgroup>
<!-- Medium -->
<colgroup class="medium"><col class="score"><col class="medal"><col class="grade"><col class="level"></colgroup>
<!-- Beast -->
<colgroup class="beast"><col class="score"><col class="medal"><col class="grade"><col class="level"></colgroup>
<thead>
<tr>
  <th rowspan="2">曲名</th>
  <th colspan="4">Light</th>
  <th colspan="4">Medium</th>
  <th colspan="4">Beast</th>
</tr>
<tr>
  <th>SCORE</th>
  <th>MDL</th>
  <th>GRD</th>
  <th>LV</th>
  <th>SCORE</th>
  <th>MDL</th>
  <th>GRD</th>
  <th>LV</th>
  <th>SCORE</th>
  <th>MDL</th>
  <th>GRD</th>
  <th>LV</th>
</tr>
</thead>
</tbody>
${scoretable}
</tbody>
</table>
<!-- content up to here -->
