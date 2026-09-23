const n = 1000;
begin
  var a: array of integer;
  var f: file of integer;
  var m: integer;
  readln(m);
  Reset(f, 'Array1000', Encoding.Default);
  SetLength(a, n);
  case m of
    1: begin
      For var i := 0 to n-1 do
      Read(f, a[i]);
    end;
    2: begin
      Seek(f, n+1);
      For var i := 0 to n-1 do
        Read(f, a[i]);
    end;
    3: begin
      Seek(f, 2*(n+1));
      For var i := 0 to n-1 do
        Read(f, a[i]);
    end;
  end;
  Close(f);
 Writeln(a);
end.