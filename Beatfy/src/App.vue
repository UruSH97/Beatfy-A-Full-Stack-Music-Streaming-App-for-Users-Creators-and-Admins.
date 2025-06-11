<script setup>
import { RouterLink, RouterView } from 'vue-router'

</script>

<template>
  <RouterView />
</template>

<style>
::-webkit-scrollbar {
    width: 8px;
  }
  
  ::-webkit-scrollbar-track {
    background: #f1f1f1;
  }
  
  ::-webkit-scrollbar-thumb {
    background: #888;
    border-radius: 30px;
  }
  
  ::-webkit-scrollbar-thumb:hover {
    background: #555;
  }

/* General styles for both scrollbars (WebKit browsers) */
::-webkit-scrollbar {
  width: 8px;
  height: 10px; /* Apply height for potential horizontal scrollbars */
}

::-webkit-scrollbar-track {
  /* background: #f1f1f1; */
  background: #243837;
}

::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 30px;
}

::-webkit-scrollbar-thumb:hover {
  background: #555;
}

/* Specific overrides for horizontal scrollbars (WebKit browsers) */
::-webkit-scrollbar-horizontal {
  height: 10px; /* Ensure height is explicitly set */
}

body {
  margin: 0;
  font-family: "Times New Roman", Times, serif;
  background-color: #F7E5DA;
  /* display: flex;
  align-items: center;
  justify-content: center; */
  height: 100vh;
}
</style>
