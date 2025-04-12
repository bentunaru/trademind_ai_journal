-- Create policy to allow public access to the screenshots bucket
CREATE POLICY "Enable public access to screenshots"
ON storage.objects FOR ALL
TO public
USING (bucket_id = 'screenshots');

-- Grant access to authenticated and anonymous users
GRANT ALL ON storage.objects TO authenticated, anon; 