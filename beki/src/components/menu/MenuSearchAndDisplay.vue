<template>
  <div>
    <b-table
      :data="searchResults"
      :columns="columns"
      :selected.sync="selected"
      focusable>
    </b-table>

    <b-button class="is-primary is-light" expanded :disabled="!selectionValid">PDF erstellen</b-button>
  </div>
</template>

<script>
import debounce from 'lodash/debounce'

export default {
  name: "MenuSearchAndDisplay",
  data() {
    return {
      selected: null,
      searchResults: [
        { id: 123, title: "Protokoll 1", inspection_date: "24.10.1996", facility: "Area 51" }
      ],
      columns: [
        {
          field: 'title',
          label: 'Titel',
          searchable: true,
        },
        {
            field: 'facility',
            label: 'Objekt',
            searchable: true,
            center: true,
        },
        {
          field: 'inspection_date',
          label: 'Prüfdatum',
          center: true
        }
      ],
      isFetching: false,
      data: [],
    }
  },
  computed: {
    selectionValid() {
      return false;
    }
  },
  methods: {
    queryProtocolTitles: debounce(function(title) {
      if (title.length === 0) {
        this.data = [];
        return;
      }

      this.isFetching = true;
      /*
      this.$http.get(`https://api.themoviedb.org/3/search/movie?api_key=bb6f51bef07465653c3e553d6ab161a8&query=${name}`)
                    .then(({ data }) => {
                        this.data = []
                        data.results.forEach((item) => this.data.push(item))
                    })
                    .catch((error) => {
                        this.data = []
                        throw error
                    })
                    .finally(() => {
                        this.isFetching = false
                    })
      */
    }, 500)
  }
}
</script>

<style>

</style>
