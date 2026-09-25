#!/usr/bin/env ruby
#
# Check for changed posts

Jekyll::Hooks.register :posts, :post_init do |post|

  commit_num = `git rev-list --count HEAD "#{ post.path }"`

  if commit_num.to_i > 1
    # Only commits dated after the publish day count as an update. Chirpy shows
    # 「更新」 whenever last_modified_at differs from date, so edits made before
    # or on the publish day would otherwise show up as updates too. The publish
    # day comes from the filename, because front matter isn't read yet at
    # post_init (and CLAUDE.md requires the two to match).
    publish_day = File.basename(post.path)[0, 10]
    lastmod_day = `git log -1 --pretty="%ad" --date=short "#{ post.path }"`.strip

    if lastmod_day > publish_day
      lastmod_date = `git log -1 --pretty="%ad" --date=iso "#{ post.path }"`
      post.data['last_modified_at'] = lastmod_date
    end
  end

end
