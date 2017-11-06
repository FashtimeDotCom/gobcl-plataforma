class FontSizes(object):
    sizes = ['xs', 's', 'default', 'l', 'xl']

    def next_size(self, size):
        size_index = self.sizes.index(size)
        next_index = size_index + 1
        if next_index > (len(self.sizes) - 1):
            return size
        else:
            return self.sizes[next_index]

    def prev_size(self, size):
        size_index = self.sizes.index(size)
        prev_index = size_index - 1
        if prev_index < 0:
            return size
        else:
            return self.sizes[prev_index]
