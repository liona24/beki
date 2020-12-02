<template>
  <!--
    This code is mostly adapted from https://github.com/buefy/buefy/blob/dev/src/components/autocomplete/Autocomplete.vue
    in order to support autocomplete for the textarea element
  -->
  <div class="autocomplete control is-expanded">
    <textarea class="textarea"
      ref="input"
      :value="value"
      @input="updateValue"
      @blur="onBlur"
      @focus="focused">
    </textarea>
    <transition name="fade">
      <div class="dropdown-menu"
        :class="{ 'is-opened-top': isOpenedTop }"
        :style="style"
        v-show="isActive && !isEmpty"
        ref="dropdown">
        <div class="dropdown-content"
          :style="contentStyle">
          <a v-for="(option, index) in data"
            :key="':' + index"
            class="dropdown-item"
            :class="{ 'is-hovered': option === hovered }"
            @click="setSelected(option, undefined, $event)">
            <span>
                {{ option }}
            </span>
          </a>
          <div class="dropdown-item is-disabled">
            Keine Übereinstimmung.
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
import { debounce } from 'lodash'

export default {
  name: "AutocompleteTextarea",
  props: {
    label: String,
    value: String,
    requestSrc: String,
    requestKey: String
  },
  data() {
    return {
      data: [],
      isFetching: false,

      selected: null,
      hovered: null,
      isActive: false,
      isListInViewportVertically: true,
      hasFocus: false,
      style: {},
    }
  },
  watch: {
    /**
     * When dropdown is toggled, check the visibility to know when
     * to open upwards.
     */
    isActive(active) {
      if (active) {
        this.calcDropdownInViewportVertical()
      } else {
        // Timeout to wait for the animation to finish before recalculating
        setTimeout(() => {
            this.calcDropdownInViewportVertical()
        }, 100)
      }
    },
  },
  computed: {
    isEmpty() {
      return !(this.data && this.data.length);
    },
    /**
     * White-listed items to not close when clicked.
     * Add input, dropdown and all children.
     */
    whiteList() {
      const whiteList = []
      whiteList.push(this.$refs.input)
      whiteList.push(this.$refs.dropdown)
      // Add all children from dropdown
      if (this.$refs.dropdown !== undefined) {
        const children = this.$refs.dropdown.querySelectorAll('*')
        for (const child of children) {
          whiteList.push(child)
        }
      }
      return whiteList
    },
    isOpenedTop() {
      return !this.isListInViewportVertically;
    },
    contentStyle() {
      return {
        maxHeight: ((width) => width === undefined ? null : (isNaN(width) ? width : width + 'px'))(this.maxHeight)
      }
    }
  },
  methods: {
    updateValue(e) {
      const value = e.target.value;

      // Close dropdown if input is clear or else open it
      if (this.hasFocus) {
        this.isActive = !!value;
      }
      if (this.isActive && value) {
        this.fetchData(value);
      }
      this.$emit("input", value);
    },
    fetchData: debounce(function(query) {
      if (query.length < 1) {
        this.data = [];
        return;
      }

      if (this.isFetching) {
        return;
      }

      this.isFetching = true;
      this.$http.post("api/_autocomplete", {
          q: query,
          key: this.requestKey,
          src: this.requestSrc
      }).then(resp => {
        this.data = resp.body;
        this.isFetching = false;
      }, () => {
        console.error("autocomplete api unavailable");
        this.isFetching = false;
      });
    }, 500),
    /**
     * Set which option is currently hovered.
     */
    setHovered(option) {
      if (option === undefined) return
      this.hovered = option
    },
    setSelected(option, closeDropdown = true, event = undefined) {
      if (option === undefined) return
      this.selected = option;
      this.$emit('input', option, event)
      if (option !== null) {
        this.setHovered(null);
      }
      closeDropdown && this.$nextTick(() => {
          this.isActive = false
      })
    },
    keydown(event) {
      const { key } = event // cannot destructure preventDefault (https://stackoverflow.com/a/49616808/2774496)
      // Close dropdown on Tab & no hovered
      this.isActive = key !== 'Tab'
      if (this.hovered === null) return
      if (this.confirmKeys.indexOf(key) >= 0) {
        // If adding by comma, don't add the comma to the input
        if (key === ',') event.preventDefault()
        // Close dropdown on select by Tab
        const closeDropdown = !this.keepOpen || key === 'Tab'
        this.setSelected(this.hovered, closeDropdown, event)
      }
    },
    /**
     * Close dropdown if clicked outside.
     */
    clickedOutside(event) {
      const target = 'shadowRoot' in this.$root.$options ? event.composedPath()[0] : event.target
      if (!this.hasFocus && this.whiteList.indexOf(target) < 0) this.isActive = false
    },
    /**
     * Calculate if the dropdown is vertically visible when activated,
     * otherwise it is openened upwards.
     */
    calcDropdownInViewportVertical() {
      this.$nextTick(() => {
        /**
         * this.$refs.dropdown may be undefined
         * when Autocomplete is conditional rendered
         */
        if (this.$refs.dropdown === undefined) return
        const rect = this.$refs.dropdown.getBoundingClientRect()
        this.isListInViewportVertically = rect.top >= 0 &&
            rect.bottom <= (window.innerHeight || document.documentElement.clientHeight)
      })
    },
    /**
     * Arrows keys listener.
     * If dropdown is active, set hovered option, or else just open.
     */
    keyArrows(direction) {
      const sum = direction === 'down' ? 1 : -1
      if (this.isActive) {
        const data = this.data.reduce((a, b) => ([...a, ...b]), [])
        let index = data.indexOf(this.hovered) + sum
        index = index > data.length - 1 ? data.length - 1 : index
        index = index < 0 ? 0 : index
        this.setHovered(data[index])
        const list = this.$refs.dropdown.querySelector('.dropdown-content')
        const element = list.querySelectorAll('a.dropdown-item:not(.is-disabled)')[index]
        if (!element) return
        const visMin = list.scrollTop
        const visMax = list.scrollTop + list.clientHeight - element.clientHeight
        if (element.offsetTop < visMin) {
            list.scrollTop = element.offsetTop
        } else if (element.offsetTop >= visMax) {
            list.scrollTop = element.offsetTop - list.clientHeight + element.clientHeight
        }
      } else {
          this.isActive = true
      }
    },
    /**
     * Focus listener.
     * If value is the same as selected, select all text.
     */
    focused(event) {
        if (this.openOnFocus) {
          this.isActive = true
        }
        this.hasFocus = true
        this.$emit('focus', event)
    },
    /**
     * Blur listener.
     */
    onBlur(event) {
      this.hasFocus = false
      this.$emit('blur', event)
    },
  },
  created() {
    if (typeof window !== 'undefined') {
      document.addEventListener('click', this.clickedOutside)
      if (this.dropdownPosition === 'auto') { window.addEventListener('resize', this.calcDropdownInViewportVertical) }
    }
  },
  mounted() {
    if (this.checkInfiniteScroll &&
      this.$refs.dropdown && this.$refs.dropdown.querySelector('.dropdown-content')
    ) {
      const list = this.$refs.dropdown.querySelector('.dropdown-content')
      list.addEventListener('scroll', () => this.checkIfReachedTheEndOfScroll(list))
    }
  },
  beforeDestroy() {
    if (typeof window !== 'undefined') {
      document.removeEventListener('click', this.clickedOutside)
      if (this.dropdownPosition === 'auto') { window.removeEventListener('resize', this.calcDropdownInViewportVertical) }
    }
    if (this.checkInfiniteScroll &&
      this.$refs.dropdown && this.$refs.dropdown.querySelector('.dropdown-content')
    ) {
      const list = this.$refs.dropdown.querySelector('.dropdown-content')
      list.removeEventListener('scroll', this.checkIfReachedTheEndOfScroll)
    }
  }
}
</script>

<style>

</style>
