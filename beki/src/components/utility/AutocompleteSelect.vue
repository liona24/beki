<template>
  <b-field :label="label" horizontal>
    <b-field>
      <b-autocomplete placeholder="Suchen ..."
        v-model="innerSearchString"

        type="search"
        icon="magnify"
        field="$repr"

        :data="data"
        :loading="isFetching"
        :required="required"
        :open-on-focus="true"
        :disabled="isWaitingForLazyResolve"

        @select="updateSelection"
        @typing="fetchData"
        @blur="makeSureSelectionIsUpdated"

        clearable
        expanded>

        <template slot="footer">
          <a class="dropdown-item" @click="() => launchEditor(false)">
            <b-icon icon="file" size="is-small"></b-icon><span> Hinzufügen ... </span>
          </a>
        </template>
      </b-autocomplete>
      <p class="control">
        <button class="button" @click="() => launchEditor(true)" :disabled="isWaitingForLazyResolve"><b-icon icon="pencil" ></b-icon></button>
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
      innerSearchString: this.value.$repr
    }
  },
  methods: {
    updateSelection(e) {
      const val = e || cloneDeep(this.initialValue);
      if((val.$status & SyncStatus.Lazy) != 0) {
        this.isWaitingForLazyResolve = true;
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
      if (edit !== true) {
        obj.$status = SyncStatus.New;
        obj.id = null;
      }
      this.$store.commit("push", {
        view: obj,
        callback: this.update,
        args: this.updateArgs
      });
    },
    makeSureSelectionIsUpdated() {
      // this method is here to check if the selection was updated
      // in the case the user *only* types the name of the element
      // he/she wishes to select without actually clicking it.
      // In this case the expected behaviour would be that the element
      // was actually selected, which we make sure of here

      if(this.$store.getters.currentViewType === this.value.$type) {
        // blurred by entering the next view, skip
        return;
      }

      const repr = this.value.$repr;
      if (repr !== this.innerSearchString) {
        const candidate = this.data.find(el => el.$repr === this.innerSearchString);
        this.updateSelection(candidate);
      }
    }
  }

}
</script>

<style>

</style>
