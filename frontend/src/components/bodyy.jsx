import React from 'react'
import { request } from '../helper/request'
import { useState } from 'react';



export default function Bodyy(){

  const [url,setUrl]=useState();
  const [summary,setSummary]=useState("");
  const [wordlimit,setWordlimit]=useState(100);

  const getSummary = async () => {
    const body = {
      url:url,
      word_limit:wordlimit
    };
    const response = await request("post", "/summarize-text", body);
  
    if (response.success) {
        setSummary(response.data?.summary);
    }
    else {
        console.log("error fetching items");
    }
}

  return (
    <div class="rest_part">
      <input class="search_bar"
        type="text"
        placeholder="search"
        onChange={(event)=>{setUrl(event.target.value)}}
      />
      <br></br>
      <button class="button"
      onClick={()=>{getSummary()}}
      >
        Search
      </button>
      <p>
        {summary}
      </p>
    </div>
  )
}
