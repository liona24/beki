<template>
  <b-loading v-if="isLoading" v-model="isLoading" :is-full-page="true" :can-cancel="false"></b-loading>
  <div v-else>
    <status-indicator :status="$store.getters.currentView.$status"></status-indicator>
    <editor-protocol-header />

    <div class="box" v-for="(entry, i) in entries" :key="i">
      <status-indicator :status="entry.$status">
        <a class="tag delete is-danger" slot="left" @click="removeEntry(i)"></a>
      </status-indicator>
      <editor-entry :index="i" />
    </div>
  </div>
</template>

<script>
import EditorProtocolHeader from '../content/editor/EditorProtocolHeader.vue'
import EditorEntry from '../content/editor/EditorEntry.vue'
import StatusIndicator from '../utility/StatusIndicator'
import { mapGetters } from 'vuex'

export default {
  components: { EditorProtocolHeader, EditorEntry, StatusIndicator },
  name: "Editor",
  data() {
    return {
      isLoading: false,
    }
  },
  computed: {
    ...mapGetters('protocol', ['entries'])
  },
  methods: {
    removeEntry(i) {
      console.log(i);
    }
  }

}
</script>

<style>

</style>
