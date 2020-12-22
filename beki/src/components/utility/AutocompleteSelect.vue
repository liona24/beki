<template>
  <b-field :label="label" horizontal>
    <b-field>
      <b-autocomplete placeholder="Suchen ..."
        v-model="innerSearchString"

        type="search"
        icon="search"
        field="$repr"

        :data="data"
        :loading="isFetching"
        :required="required"
        :open-on-focus="true"
        :disabled="isWaitingForLazyResolve"

        @select="updateSelection"
        @typing="fetchData"

        clearable
        expanded>

        <template slot="footer">
          <a class="dropdown-item" @click="() => launchEditor(false)">
            <b-icon icon="file" size="is-small"></b-icon><span> Hinzufügen ... </span>
          </a>
        </template>
      </b-autocomplete>
      <p class="control">
        <button class="button" @click="() => launchEditor(true)" :disabled="isWaitingForLazyResolve"><b-icon icon="edit" ></b-icon></button>
      </p>
      <p class="control">
        <button class="button" @click="() => launchEditor(false)" :disabled="isWaitingForLazyResolve"><b-icon icon="file" ></b-icon></button>
      </p>
    </b-field>
  </b-field>
</template>

<script>
import { SyncStatus } from '../../store/common'
import { debounce, cloneDeep } from 'lodash'

export default {
  name: "AutocompleteSelect",
  props: {
    required: {
      type: Boolean,
      default: false
    },
    label: String,

    requestSrc: String,

    value: Object,

    update: String,
    updateArgs: {
      type: Object,
      default() {
        return {}
      }
    }
  },
  data() {
    return {
      initialValue: cloneDeep(this.value),
      data: [],
      isWaitingForLazyResolve: false,
      isFetching: false,
      ignoreNextSelection: false,
    }
  },
  computed: {
    innerSearchString: {
      get() {
        return this.value.$repr;
      },
      set() {
        // buefy is a little shitty with state managment and side effects thereof.
        // therefor we cannot v-bind this.value directly to <b-autocomplete> but
        // have to opt out for an "representation" of it
        // Anyway <b-autocomplete> will still try to set this value, but since
        // <b-autocomplete> duplicates the state nevertheless we do not need to
        // update it.
      }
    }
  },
  methods: {
    updateSelection(e) {
      if (this.ignoreNextSelection) {
        this.ignoreNextSelection = false;
        return;
      }

      const val = e || cloneDeep(this.initialValue);
      if((val.$status & SyncStatus.Lazy) != 0) {
        this.isWaitingForLazyResolve = true;
        // TODO: it seems questionable why we need a recursive fetch here
        this.$http.get(`api/${this.requestSrc}/${val.id}/recursive`).then(resp => {
          this.$store.commit(this.update, { val: resp.body, ...this.updateArgs });
        }).finally(() => {
          this.isWaitingForLazyResolve = false;
        });
      } else {
        this.$store.commit(this.update, { val: val, ...this.updateArgs });
      }
    },
    fetchData: debounce(function(query) {
      if (query.length < 1) {
        this.data = [];
        return;
      }

      this.isFetching = true;

      this.$http.post("api/_discover", {
          q: query,
          src: this.requestSrc,
      }).then(resp => {
        this.data = resp.body;
      }, () => {
        console.error("discover api unavailable");
      }).finally(() => {
        this.isFetching = false;
      });
    }, 500),
    launchEditor(edit) {
      const obj = cloneDeep(this.value);
      if (obj.$status === SyncStatus.Empty || edit !== true) {
        obj.$status = SyncStatus.New;
        obj.id = null;
      }

      // HACK: Prevent bubbling of the select(null) event
      // after we force the update of innerSearchString
      this.ignoreNextSelection = true;

      this.$store.commit("push_overlay", {
        view: obj,
        callback: this.update,
        args: this.updateArgs
      });
    },
  }

}
</script>

<style>

</style>
