<!-- content from here -->
<h3>ユーザ情報</h3>
<form accept-charset="UTF-8" action="" method="post" autocomplete="off">
  <p>${message}</p>
  <p>Username: ${username}</p>
  <p><label for="nickname">Nickname</label><br>
     <input type="text" name="nickname" value="${nickname}"></p>
  <p><label for="comment">Comment</label><br>
     <input type="text" name="comment" value="${comment}"></p>
  <p><input type="checkbox" name="ispublic" value="True" ${ispublic}>
     <label for="ispublic">スコアデータを公開する<br>(<a href="${url}">${url_label}</a>で外部から閲覧可能にします)</label></p>
     
  <p><input type="submit" value="決定"></p>
</form>
<!-- content up to here -->
