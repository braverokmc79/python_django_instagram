



export const postsHtmlTemplate =(post)=>{
    return `
          <article class="w-3/4 border rounded-lg border-gray-300 mx-auto shadow-lg bg-white">
            
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
               ${post.author.id ? `
                  <div class="flex items-center space-x-5">
                    <i class="fa fa-pencil fa-lg text-gray-500 cursor-pointer hover:text-gray-800"
                     onclick="postUpdatePage('${post.id}', '${post.csrf_token}', this)"
                    
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
                <span class="text-gray-600">${post.caption}</span>
              </div>
            </div>
          
            <!-- 댓글 영역 -->
            <div class="border-t border-gray-200 p-4 mt-5">
              <h3 class="font-bold text-lg text-gray-800 mb-3">댓글</h3>
              ${post.comment_post.map(comment => `
                <p id="comment-${comment.id}" class="text-sm text-gray-700 mb-3 border-b pb-2 flex justify-between">
                  <span>
                    <span class="font-semibold text-gray-800 mr-2">${comment.author.username}</span>
                    <span>${comment.contents}</span>
                  </span>
                  ${userId ==comment.author.id ? `
                    <span class="font-semibold text-gray-800 mr-3"
                    onclick="commentDelete('${comment.id}', '${post.csrf_token}', this)"
                    >
                      <i class="fa fa-trash-o fa-lg text-red-500 cursor-pointer hover:text-red-700"></i>
                    </span>
                  ` : ''}
                </p>
              `).join('')}
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



