begin
  var f: file of integer;
  var t: text;
  
  Rewrite(t, 'Массивы.txt');
  Rewrite(f, 'Array64', Encoding.Default);
  Writeln(t,'64 элемента');
  Writeln(t);
  Writeln(t, 'Лучший случай:');
  Writeln(t);
  for var i := -32 to 31 do begin
    var j :=i+random(-5,5);
    Write(f,j);
    Write(t,j, ' ');
  end;
  Writeln(t);
  Write(F, -1000000);
  Writeln(t);
  Writeln(t, 'Средний случай:');
  Writeln(t);
  for var i := -32 to 31 do begin
    var j :=i+random(-64, 64);
    Write(f,j);
    Write(t,j, ' ');
  end;
  Writeln(t);
  Write(F, -1000000);
  Writeln(t);
  Writeln(t, 'Худший случай:');
  Writeln(t);
  for var i := 31 downto -32 do begin
    var j :=i+random(-5,5);
    Write(f,j);
    Write(t,j, ' ');
  end;
  Writeln(t);
  Writeln(t);
  Writeln(t,'_'*1000);
  Writeln(t);
  Close(f);
  Rewrite(f, 'Array1000');
  Writeln(t, '1000 элементов');
  Writeln(t);
  Writeln(t, 'Лучший случай:');
  Writeln(t);
  for var i := -500 to 499 do begin
    var j :=i+random(-10,10);
    Write(f,j);
    Write(t,j, ' ');
  end;
  Writeln(t);
  Write(F, -1000000);
  Writeln(t);
  Writeln(t, 'Средний случай:');
  Writeln(t);
  for var i := -500 to 499 do begin
    var j :=i+random(-1000,1000);
    Write(f,j);
    Write(t,j, ' ');
  end;
  Writeln(t);
  Write(F, -1000000);
  Writeln(t);
  Writeln(t, 'Худший случай:');
  Writeln(t);
  for var i := 499 downto -500 do begin
    var j :=i+random(-10,10);
    Write(f,j);
    Write(t,j, ' ');
  end;
  Writeln(t);
  Writeln(t,'_'*1000);
  Writeln(t);
  Close(f);
  Rewrite(f, 'Array10000-100000');
  Writeln(t, '10000-100000 элементов');
  Writeln(t);
  Writeln(t, 'Лучший случай:');
  Writeln(t);
  for var i := -10000 to 9999 do begin
    var j :=i+random(-50,50);
    Write(f,j);
    Write(t,j, ' ');
  end;
  Writeln(t);
  Write(F, -1000000);
  Writeln(t);
    Writeln(t, 'Средний случай:');
  Writeln(t);
  for var i := -10000 to 9999 do begin
    var j :=i+random(-10000,9999);
    Write(f,j);
    Write(t,j, ' ');
  end;
  Writeln(t);
  Write(F, -1000000);
  Writeln(t);
  Writeln(t, 'Худший случай:');
  Writeln(t);
  for var i := 9999 downto -10000 do begin
    var j :=i+random(-50,50);
    Write(f,j);
    Write(t,j, ' ');
  end;
  
end.