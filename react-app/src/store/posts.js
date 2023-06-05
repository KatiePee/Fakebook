const ALL_POSTS = 'post/allPosts'
const SINGLE_POST = 'post/singlePosts'

const allPostsAction = (posts) => ({
  type: ALL_POSTS,
  payload: posts
})

const singlePostAction = (post) => ({
  type: SINGLE_POST,
  payload: post
})

export const allPostsThunk = () => async dispatch => {
  console.log("all posts thunk being called")
  const res = await fetch("/api/posts/", {
    headers: {
			"Content-Type": "application/json",
		},
  })

  // console.log("-----RES IN THUNK--------", res)
  // console.log('-------------------- all post thunk -- res------------------', res)
  if (res.ok) {
    const posts = await res.json()
    console.log("--------INSIDE THUNK---------- ",posts);
    console.log("posts", posts)
    dispatch(allPostsAction(posts))
    return res
  } else return null
}

export const singlePostThunk = (postId) => async dispatch => {
  const res = await fetch(`/api/posts/${postId}`);
  if (res.ok) {
    const post = await res.json()
    dispatch(singlePostAction(post))
    return res
  } else {
    const errors = await res.json();
    return errors;
  }
}

// const initialState = { allPosts: {}, singlePost: {} }
const initialState = { }
const postReducer = (state = initialState, action) => {
  // let newState;
  switch (action.type) {
    case ALL_POSTS:

      console.log("PAYLOAD IN POST STATE REDUCER",action.payload)
      let someState = {}
      action.payload.forEach(post => {
        someState[post.id] = post
      })
      return { allPosts: someState, ...state}
      // newState.allPosts = {...state,  allPosts: action.payload }
      // return newState
    default:
      return state;
  }
}

export default postReducer
// const CREATE_POST = "posts/CREATE_POST";

// const createPostAction = (post) => {
//   return {
//     type: CREATE_POST,
//     post
//   };
// };

// export const createPostThunk = (content) => async (dispatch) => {
//   const response = await fetch("/api/spots/new", {
//     method: "POST",
//     headers: {
//       "Content-Type": "application/json",
//     },
//     body: JSON.stringify({
//       content,
//       // add ability to add photos
//     }),
//   });

//   if (response.ok) {
//     const data = await response.json();
//     dispatch(createPostAction(data));
//   } else {
//     return "Cannot Create A New Post!";
//   }
// };


// export default function postReducer(state = initialState, action) {
//     switch (action.type) {
//         case CREATE_POST:
//            pass
//     }
// }
