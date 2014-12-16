<!-- content from here -->
<h3>ユーザ情報</h3>
<form accept-charset="UTF-8" action="" method="post">
  <p>${message}</p>
  <p>Username: ${username}</p>
  <p><label for="nickname">Nickname</label><br>
     <input type="text" name="nickname" value="${nickname}"></p>
  <p><label for="comment">Comment</label><br>
     <input type="text" name="comment" value="${comment}"></p>
  <p><label for="ispublic">スコアデータを公開する</label><br>
     <input type="checkbox" name="ispublic" value="True" ${ispublic}></p>
  <p><input type="submit" value="決定"></p>
</form>
<!-- content up to here -->