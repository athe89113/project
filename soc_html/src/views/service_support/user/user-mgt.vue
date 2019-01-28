<template>
  <user-list :company-id="companyId"></user-list>
</template>
<script>
  import userList from './user-list.vue'
  export default {
    data: function () {
      return {
        companyId: ""
      }
    },
    ready: function () {
    },
    methods: {},
    components: {
      userList
    }
  }
</script>