let loading = false; // 로딩 중 여부
const container = document.querySelector('#postList'); // 게시글 컨테이너


const loadMorePosts = async () => {
  if (loading) return;
  loading = true;

  try {
    const response = await fetch(`/api/posts/?format=json`);
    const data = await response.json();
  
    // 데이터 추가\
    data.posts.forEach(post => {
      const postElement =postsHtmlTemplate(post, data.loginUser);     
      container.insertAdjacentHTML('beforeend', postElement);
    });


  } catch (error) {
    console.error("Error loading posts:", error);
  } finally {
    loading = false;
  }

};


//게시글 로드
loadMorePosts(); 



  //게시글 삭제
  async function postDelete(postId,csrfToken, target) {
    if(confirm("정말 삭제 하시겠습니까?")){
        try {
          const response = await fetch(`/posts/${postId}/post_delete/`, {
            method: "DELETE",
            headers: {
              "X-CSRFToken": csrfToken,
            },
          });
          const data = await response.json();
      
          if (response.ok && data.success) {
            alert(data.message);
            // 삭제된 댓글 UI에서 제거
            
            target.closest('article').remove();  // 댓글 부모 article 요소를 삭제   
          } else {
            alert(data.message || "댓글 삭제 중 오류가 발생했습니다.");
          }
        } catch (error) {
          console.error("댓글 삭제 중 오류:", error);
        }

    }
}






//댓글 생성
async function commentCreate(postId, csrfToken, event) {
    event.preventDefault();
  
    // 이벤트가 발생한 요소에서 가장 가까운 form 요소 찾기
    const form = event.currentTarget.closest('form');
    const contents = form.querySelector('textarea[name="contents"]').value.trim();
    if (!contents) {
      alert("댓글을 입력하세요.");
      return;
    }

  try {
    const response = await fetch(`/posts/${postId}/comment_create/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-CSRFToken': csrfToken,
      },
      body: new URLSearchParams({ contents }),
    });

    const data = await response.json();
    console.log("댓글 등록후 반환 데이터 :", data);
    
    if (data.success) {
      console.log("댓글 등록후 반환된 데이터 :", data);
      const articleElement = document.querySelector(`#article-${postId}`);
      const commentListElementContainer = articleElement.querySelector(`.comment-list`);          
      commentListElementContainer.insertAdjacentHTML('afterbegin', commentListElement(data.comment, csrfToken, data.comment.author.username));
      form.reset();
    }

 
    if (data.errors) {
      alert(data.errors);
    }
  } catch (error) {
    console.error('댓글 등록 중 오류 발생:', error);
    alert('댓글 등록에 실패했습니다.');
  }
}




//댓글 삭제 처리
async function commentDelete(commentId,csrfToken, target){
  if(confirm("정말 삭제 하시겠습니까?")){
    try{
      const response = await fetch(`/posts/${commentId}/comment_delete/`,{
        method:"DELETE",
        headers:{
          'X-CSRFToken':csrfToken
        }
      });

      const data = await response.json();
      
      if(!response.ok) throw new Error(data.error);
      
      if(data.success){
        target.closest(`#comment-${commentId}`).remove();  // 댓글 부모 요소를 삭제   
      }              
      
    }catch(error){
      console.error("댓글 삭제 실패 ",error);
    }
  }
}


// 수정페이지 이동
function postUpdatePage(postId){
  window.location.href = `/posts/${postId}/post_update/`;
}







//// 게시글 템플릿
const postsHtmlTemplate =(post,loginUser)=>{
  return `
        <article class="w-3/4 border rounded-lg border-gray-300 mx-auto shadow-lg bg-white" id="article-${post.id}">
          
          <!-- 상단 프로필 영역 -->
          <div class="w-full flex justify-between items-center border-b border-gray-200 p-4">
            
            <!-- 왼쪽 콘텐츠 -->
            <div class="flex items-center space-x-3">
              <span>
                ${post.author.profile_photo ? 
                  `<img src="${post.author.profile_photo}" class="w-12 h-12 rounded-full border border-gray-300">` :
                  `<img src="/static/images/posts/no_avatar.png" class="w-12 h-12 rounded-full border border-gray-300">`}
              </span>
              <span class="font-semibold text-gray-800 text-lg" >${post.author.username}</span>
            </div>
            
            <!-- 오른쪽 콘텐츠 -->
             ${(post.author.username===loginUser) ? `
                <div class="flex items-center space-x-5">
                  <i class="fa fa-pencil fa-lg text-gray-500 cursor-pointer hover:text-gray-800"
                   onclick="postUpdatePage('${post.id}')"
                  
                  ></i>
                  <i class="fa fa-trash-o fa-lg text-red-500 cursor-pointer hover:text-red-700"
                  onclick="postDelete('${post.id}', '${post.csrf_token}', this)"
                  ></i>
                </div>
              ` :''
             }
          </div>
        
          <!-- 포스트 이미지 -->
          <div class="w-full">
            <img class="w-full h-96 object-contain bg-gray-100" src="${post.image}" alt="Post image">
          </div>
        
          <!-- 설명 및 좋아요 -->
          <div class="p-4">    
          <div class="flex items-center space-x-3" 
            id="like-button-${post.id}"
            onclick="debouncedHandleLikeClick('${post.id}', '${post.csrf_token}', this)">         
              ${post.image_likes.includes(Number(userId)) ? 
                `<i class="fa fa-heart fa-2x text-red-500  cursor-pointer hover:text-red-500"></i>`  :
                `<i class="fa fa-heart-o fa-2x text-gray-500 cursor-pointer hover:text-red-500"></i>`              
            } (<span id="like-count-${post.id}" class="mx-0 !mx-0">${post.image_likes.length}</span>)
  
         </div>
  
  
            <div class="mt-5">
              <b class="text-gray-800">${post.author.username}</b>
              <span class="text-gray-600 break-all">${post.caption}</span>
            </div>
          </div>
        
          <!-- 댓글 영역 -->
          <div class="border-t border-gray-200 p-4 mt-5">
            <h3 class="font-bold text-lg text-gray-800 mb-3">댓글</h3>
            <div class="comment-list">
              ${post.comment_post.map(comment => commentListElement(comment, post.csrf_token, loginUser) ).join('')}
            </div>
          </div>

        
          <!-- 댓글 입력 폼 -->
          <div class="mt-5 p-4">
            <form action="#" method="post" class="flex flex-col space-y-4" 
                onSubmit="commentCreate('${post.id}', '${post.csrf_token}', event)" >
              <textarea name="contents" class="p-2 border rounded-lg w-full" placeholder="댓글을 입력하세요" required ></textarea>
              <button type="submit" class="px-4 py-2 bg-indigo-500 text-white font-semibold rounded-lg hover:bg-indigo-600">
                댓글 등록
              </button>
            </form>
          </div>        
        </article>
        `;
}


//댓글 목록 템플릿
const commentListElement = (comment, csrf_token, loginUser) => {
  return `<p id="comment-${comment.id}" class="text-sm text-gray-700 mb-3 border-b pb-2 flex justify-between">
    <span>
      <span class="font-semibold text-gray-800 mr-2">${comment.author.username}</span>
      <span class="break-all">${comment.contents} </span>
    </span>
    ${(loginUser===comment.author.username) ? `
      <span class="font-semibold text-gray-800 mr-3"
      onclick="commentDelete('${comment.id}', '${csrf_token}', this)">
        <i class="fa fa-trash-o fa-lg text-red-500 cursor-pointer hover:text-red-700"></i>
      </span>
    ` : ''}
  </p> `;

}