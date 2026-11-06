-- Haq: accounts, saved cases, reminders, private evidence storage.
-- Paste this whole file into Supabase → SQL Editor → New query → Run. Safe to run more than once.
-- Security model: every row belongs to auth.uid(); row-level security lets a user touch ONLY their own data.

create table if not exists public.profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  full_name text,
  city text,
  language text,
  email_reminders boolean not null default true,
  updated_at timestamptz not null default now()
);

create table if not exists public.cases (
  id uuid primary key,
  user_id uuid not null default auth.uid() references auth.users(id) on delete cascade,
  title text,
  category text,
  status text not null default 'new',
  data jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
create index if not exists cases_user_idx on public.cases(user_id, updated_at desc);

create table if not exists public.reminders (
  id bigserial primary key,
  user_id uuid not null default auth.uid() references auth.users(id) on delete cascade,
  case_id uuid not null references public.cases(id) on delete cascade,
  case_title text,
  label text not null,
  due_date date not null,
  basis text,
  sent jsonb not null default '{}'::jsonb,   -- e.g. {"7": "2026-11-19", "1": "2026-11-25"}
  created_at timestamptz not null default now()
);
create index if not exists reminders_due_idx on public.reminders(due_date);

alter table public.profiles  enable row level security;
alter table public.cases     enable row level security;
alter table public.reminders enable row level security;

drop policy if exists "own profile" on public.profiles;
create policy "own profile" on public.profiles for all using (auth.uid() = id) with check (auth.uid() = id);

drop policy if exists "own cases" on public.cases;
create policy "own cases" on public.cases for all using (auth.uid() = user_id) with check (auth.uid() = user_id);

drop policy if exists "own reminders" on public.reminders;
create policy "own reminders" on public.reminders for all using (auth.uid() = user_id) with check (auth.uid() = user_id);

-- Private storage bucket for evidence files: path = <user_id>/<case_id>/<file_id>
insert into storage.buckets (id, name, public, file_size_limit)
values ('evidence', 'evidence', false, 8388608)
on conflict (id) do nothing;

drop policy if exists "evidence own read"   on storage.objects;
drop policy if exists "evidence own write"  on storage.objects;
drop policy if exists "evidence own update" on storage.objects;
drop policy if exists "evidence own delete" on storage.objects;
create policy "evidence own read"   on storage.objects for select using (bucket_id = 'evidence' and (storage.foldername(name))[1] = auth.uid()::text);
create policy "evidence own write"  on storage.objects for insert with check (bucket_id = 'evidence' and (storage.foldername(name))[1] = auth.uid()::text);
create policy "evidence own update" on storage.objects for update using (bucket_id = 'evidence' and (storage.foldername(name))[1] = auth.uid()::text);
create policy "evidence own delete" on storage.objects for delete using (bucket_id = 'evidence' and (storage.foldername(name))[1] = auth.uid()::text);
