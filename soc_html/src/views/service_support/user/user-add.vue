<template>
  <user-add-base :company-id="companyId"></user-add-base>
</template>

<script>
  import userAddBase from "./user-add-base.vue"
  export default {
    data: function () {
      return {
        companyId: ""
      }
    },
    ready: function () {
    },
    methods: {
    },
    components: {
      userAddBase
    }
  }
</script>