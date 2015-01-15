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
<thead>
<tr>
  <th></th>
  <th colspan="4">Light</th>
  <th colspan="4">Medium</th>
  <th colspan="4">Beast</th>
</tr>
<tr>
  <th>曲名</th>
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
