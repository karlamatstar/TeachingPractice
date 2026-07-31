import axios from 'axios';

const baseApi = axios.create({
	headers: {
		'Content-Type': 'application/json'
	},
	baseURL: 'http://localhost:33000',
	withCredentials: true,
	timeout: 1000 * 30
});

baseApi.interceptors.response.use()

baseApi.interceptors.response.use(
	function (response) {
		// Any status code that lie within the range of 2xx cause this function to trigger
		// Do something with response data
		return response;
	},
	function (error) {
		if (error.status === 403) {
			alert("토큰 만료로 로그인 페이지로 이동합니다.");
			localStorage.removeItem("accessToken");
			localStorage.removeItem("user");
			window.location.replace("/");
		}
		// Any status codes that falls outside the range of 2xx cause this function to trigger
		// Do something with response error
		return Promise.reject(error);
	}
);


export default baseApi;