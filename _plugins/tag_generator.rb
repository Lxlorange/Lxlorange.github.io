#!/usr/bin/env ruby
#
# Custom tag page generator that produces English URL slugs.
# Replaces jekyll-archives for tag pages.
# Uses _data/tag_slugs.yml to map Chinese tag names to English slugs.
# English-only tags pass through as-is (lowercased, hyphenated).

module Jekyll
  class TagPageGenerator < Generator
    safe true
    priority :low

    def generate(site)
      return unless site.layouts.key? 'tag'

      tag_slugs = site.data['tag_slugs'] || {}

      site.tags.each do |tag_name, posts|
        slug = tag_to_slug(tag_name, tag_slugs)
        next if slug.nil? || slug.empty?

        site.pages << TagPage.new(site, site.source, tag_name, slug, posts)
      end
    end

    private

    def tag_to_slug(tag_name, tag_slugs)
      # 1. Explicit mapping
      return tag_slugs[tag_name] if tag_slugs.key?(tag_name)

      # 2. Already ASCII-safe — just normalize
      ascii = tag_name.downcase
              .gsub(/[\s_]+/, '-')
              .gsub(/[^a-z0-9\-]/, '')
              .gsub(/-{2,}/, '-')
              .gsub(/^-|-$/, '')

      return ascii unless ascii.empty?

      # 3. Contains only non-Latin characters and not mapped — this is a problem.
      #    Generate a warning slug so the author knows to add a mapping.
      Jekyll.logger.warn "TagPageGenerator:",
        "Tag '#{tag_name}' has no English slug mapping. " \
        "Add it to _data/tag_slugs.yml. Using fallback slug."
      # Fallback: first 8 chars of hex digest
      require 'digest'
      "tag-#{Digest::MD5.hexdigest(tag_name)[0, 8]}"
    end
  end

  class TagPage < Page
    def initialize(site, base, tag_name, slug, posts)
      @site = site
      @base = base
      @dir  = File.join('tags', slug)
      @name = 'index.html'

      process(@name)
      read_yaml(File.join(base, '_layouts'), 'tag.html')

      self.data['title'] = tag_name
      self.data['posts'] = posts
      self.data['permalink'] = "/tags/#{slug}/"
    end
  end
end
