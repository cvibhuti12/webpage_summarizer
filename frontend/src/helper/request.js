import axios from 'axios';

axios.defaults.baseURL = 'http://localhost:8080';

export const request = async (method, url, data) => {
    try {
        const response = await axios({
            method: method,
            url: url,
            data: data
        });
        return { success: true, data: response.data };
    }
    catch (err) {
        console.log(err);
        return { success: false, data: {} };
    }
};