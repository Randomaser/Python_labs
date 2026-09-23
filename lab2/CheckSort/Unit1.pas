Unit Unit1;

interface

uses System, System.Drawing, System.Windows.Forms;

const MINIMUM = 32;

type
  Form1 = class(Form)
    procedure comboBox1_SelectedIndexChanged(sender: Object; e: EventArgs);
    procedure button1_Click(sender: Object; e: EventArgs);
    procedure label2_Click(sender: Object; e: EventArgs);
    procedure label4_Click(sender: Object; e: EventArgs);
    procedure comboBox2_SelectedIndexChanged(sender: Object; e: EventArgs);
    procedure label6_Click(sender: Object; e: EventArgs);
    procedure button2_Click(sender: Object; e: EventArgs);
    procedure button3_Click(sender: Object; e: EventArgs);
    procedure button4_Click(sender: Object; e: EventArgs);
    procedure button5_Click(sender: Object; e: EventArgs);
    procedure label10_Click(sender: Object; e: EventArgs);
    procedure button6_Click(sender: Object; e: EventArgs);
   { procedure label11_Click(sender: Object; e: EventArgs);}
    procedure label11_Click(sender: Object; e: EventArgs);
  {$region FormDesigner}
  internal
    {$resource Unit1.Form1.resources}
    comboBox1: ComboBox;
    button1: Button;
    label1: &Label;
    label2: &Label;
    comboBox3: ComboBox;
    label3: &Label;
    label4: &Label;
    label5: &Label;
    label6: &Label;
    label7: &Label;
    label8: &Label;
    button2: Button;
    label9: &Label;
    button3: Button;
    label10: &Label;
    button4: Button;
    button5: Button;
    button6: Button;
    label11: &Label;
    components: System.ComponentModel.IContainer;
    comboBox2: ComboBox;
    {$include Unit1.Form1.inc}
  {$endregion FormDesigner}
  public
    constructor;
    begin
      InitializeComponent;
    end;
  end;

function SortPus(arr: array of integer; var count: Integer): array of integer;
procedure bogo(var a: array of integer; var count: integer);
function sorted(a: array of integer): boolean;
procedure shuffle(var a: array of integer);
function find_minrun(n: integer): integer;
procedure insertation_sort(var arr: array of integer; left, right: integer; var count: integer);
procedure merge(var arr: array of integer; l, m, r: integer; var count: integer);
procedure tim_sort(var arr: array of integer;var count: integer);
procedure merge_sort(var arr: array of integer; l, m, r: integer; var count: integer);
procedure shell_sort(var a: array of integer; var count: integer);
procedure input_sort(var a: array of integer; var count: integer);
procedure piramid_Sort(var A: array of integer; Count: Integer; var count_c: integer);
procedure gnomesort(var arr: array of integer; var count: Integer);
procedure radix_sort(var arr: array of integer; var count: integer);

implementation

{Сортировка Пузырьком}
function SortPus(arr: array of integer; var count: Integer): array of integer;
var vrem, i:integer;
    f: boolean;
begin
  var n := length(arr);
  i := 0;
  repeat
    f := true;
    for var j := n-2 downto i do begin
      count += 1;
      if arr[j] > arr[j+1] then begin
        vrem := arr[j];
        arr[j] := arr[j+1];
        arr[j+1] := vrem;
        f := false;
      end;
    end;
    i += 1;
    until (f) or (i = n-1);
    Result := arr;
end;

{Болотная Сортировка}

procedure shuffle(var a: array of integer);
var
  k,tmp: integer;
begin
  for var i := (a.Length-1) downto 0 do begin
     k := PABCSystem.random(i) + 1;
     if (a[i] <> a[k]) then begin
       tmp := a[i]; a[i] := a[k]; a[k] := tmp
     end
  end
end;

function sorted(a: array of integer): boolean;
begin
  sorted := True;
  for var i := 1 to a.Length-1 do
    if (a[i - 1] > a[i]) then begin
      sorted := False; exit
    end
end;

procedure bogo(var a: array of integer; var count: integer);
begin
  while not sorted(a) do begin
    shuffle(a);
    count += 1;
    if count > 100000000 then
      break;
  end
end;

{TimSort}

function find_minrun(n: integer): integer;
begin
  var r := 0;
  while n > MINIMUM do begin
    r := r or n and 1;
    n := n shr 1;
  end;
  Result := n + r;
end;

{TimSort/Сортировка вставками}

procedure insertation_sort(var arr: array of integer; left, right: integer; var count:integer);
begin
  for var i := left+1 to right do begin
    var element := arr[i];
    var j := i - 1;
    try
    while (element < arr[j]) and (j>=left) do begin
      count += 1;
      arr[j+1] := arr[j];
      j -= 1;
    end;
    except
    end;
    arr[j+1] := element;
  end;
end;

procedure merge(var arr: array of integer; l, m, r: integer; var count: integer);
var left, right: array of integer;
begin
  var array_length1 := m-l+1;
  var array_length2 := r-m;
  setlength(left, array_length1);
  setlength(right, array_length2);
  for var i := 0 to array_length1-1 do
    left[i] := arr[l+i];
  for var i := 0 to array_length2-1 do
    right[i] := arr[m+i+1];
  var i := 0;
  var j := 0;
  var k := l;
  while (j < array_length2) and (i < array_length1) do begin
    count += 1;
    if left[i] <= right[j] then begin
      arr[k] := left[i];
      i += 1;
    end
    else begin
      arr[k] := right[j];
      j += 1;
    end;
    k += 1
  end;
  while i < array_length1 do begin
    arr[k] := left[i];
    count += 1;
    k += 1;
    i += 1;
  end;
  while j < array_length2 do begin
    arr[k] := right[j];
    count += 1;
    k += 1;
    j += 1;
  end;
end;

procedure tim_sort(var arr: array of integer; var count: integer);
begin
  var n := Length(arr);
  var minrun := find_minrun(n);
  
  var start := 0;
  while start < n do begin
    var ends := min(start+minrun-1, n-1);
    insertation_sort(arr, start, ends, count);
    start += minrun;
  end;
  var size := minrun ;
    while size < n do begin
      var left := 0; 
      while left < n do begin
        var mid := min(n - 1, left + size - 1);
        var right := min((left + 2 * size - 1), (n - 1)); 
        merge(arr, left, mid, right, count);
        left += size*2;
      end;
      size := 2 * size;
    end;
end;

{Сортировка слиянием}

procedure merge_sort(var arr: array of integer; l, m, r: integer; var count: integer);
var left, right: array of integer;
begin
  var array_length1 := m-l+1;
  var array_length2 := r-m;
  setlength(left, array_length1);
  setlength(right, array_length2);
  for var i := 0 to array_length1-1 do
    left[i] := arr[l+i];
  if left.Length > 2 then
    merge_sort(left, 0, left.Length div 2, left.Length-1,count)
  else if left[0] > left[1] then begin
    var tmp := left[0];
    left[0] := left[1];
    left[1] := tmp;
  end;
  for var i := 0 to array_length2-1 do
    right[i] := arr[m+i+1];
  if right.Length > 2 then
    merge_sort(right, 0, right.Length div 2, right.Length-1, count)
  else try if right[0] > right[1] then begin
    var tmp := right[0];
    right[0] := right[1];
    right[1] := tmp;
    end;
    except;
    end;
  var i := 0;
  var j := 0;
  var k := l;
  while (j < array_length2) and (i < array_length1) do begin
    count += 1;
    if left[i] <= right[j] then begin
      arr[k] := left[i];
      i += 1;
    end
    else begin
      arr[k] := right[j];
      j += 1;
    end;
    k += 1
  end;
  while i < array_length1 do begin
    arr[k] := left[i];
    count += 1;
    k += 1;
    i += 1;
  end;
  while j < array_length2 do begin
    arr[k] := right[j];
    count += 1;
    k += 1;
    j += 1;
  end;
end;

{Сортировка Шелла}

procedure shell_sort(var a: array of integer; var count: integer);
var n, i, step, c : integer;
    boo: boolean;
begin
  n := a.Length;
  step := n div 2;
  while step>0 do
        begin
             for var j:=0 to n-step-1 do
                 begin
                      i := j;
                      while ((i>-1) and (a[i]>a[i+1])) do
                            begin
                                 c := a[i];
                                 a[i] := a[i+step];
                                 a[i+step] := c;
                                 i := i - 1;
                                 count += 1;
                                 boo := True;
                            end;
                      if not Boo then
                        count += 1;
                 end;
             step := step div 2;
        end;
end;

{Сортировка методом выбора}

procedure input_sort(var a: array of integer; var count: integer);
var n := a.Length;
var k, m: integer;
begin
   for var i:= n-1 downto 1 do
     //задаем длину рассматриваемой части массива
      begin
        //ищем максимальный элемент и его номер
        k:=i; m:=a[i];         
        for var j:= 0 to i-1 do begin
          count += 1;
          if a[j] > m 
          then 
             begin 
             k:=j; m:=a[k]
             end;
        end;
               //меняем местами найденный элемент и последний
                if k <> i 
                then
                  begin 
                  a[k]:=a[i]; 
                  a[i]:= m;
                  end;
       end;
end;

{Пирамидальная сортировка}

procedure piramid_Sort(var A: array of integer; Count: Integer; var count_c: integer);
  procedure DownHeap(index, Count: integer; Current: integer);
  {Функция пробегает по пирамиде восстанавливая ее
  Также используется для изначального создания пирамиды
  Использование: Передать номер следующего элемента в index
  Процедура пробежит по всем потомкам и найдет нужное место для следующего элемента}
  var
    Child: Integer;
  begin
    while index < Count div 2 do
     begin
      count_c += 1;
      Child := (index+1)*2-1;
      if (Child < Count-1) and (A[Child] < A[Child+1]) then
        Child:=Child+1;
      if Current >= A[Child] then
        break;
      A[index] := A[Child];
      index := Child;
    end;
    A[index] := Current;
  end;
 
{Основная функция }
var
  Current: integer;
begin
  {Собираем пирамиду}
  for var i := (Count div 2)-1 downto 0 do
    DownHeap(i, Count, A[i]);
  {Пирамида собрана. Теперь сортируем}
  for var i := Count-1 downto 0 do begin
    Current := A[i];
    count_c += 1;{перемещаем верхушку в начало отсортированного списка}
    A[i] := A[0];
    DownHeap(0, i, Current);{находим нужное место в пирамиде для нового элемента}
  end;
end;

{Сортировка гномиком}

procedure gnomesort(var arr: array of integer; var count: Integer);
var
  size, i, j, t: Integer;
begin
  size := arr.Length;
  i := 1;
  j := 2;
  while i <= size-1 do
  begin
    count += 1;
    if arr[i - 1] < arr[i] then
    begin
      i := j;
      j := j + 1
    end
    else
    begin
      t := arr[i - 1];
      arr[i - 1] := arr[i];
      arr[i] := t;
      i := i - 1;
      if i = 0 then
      begin
        i := j;
        j := j + 1
      end;
    end;
  end;
end;

{Поразрядная}

procedure radix_sort(var arr: array of integer; var count: integer);
begin
  var lengths := length(IntToStr(max(arr)));
  var rand := 10;
  for var i := 0 to lengths-1 do begin
    var vrem_arr: array of array of integer;
    SetLength(vrem_arr, rand);
    for var j := 0 to rand-1 do
      SetLength(vrem_arr[j], 0);
    foreach var x in arr do begin
      count += 1;
      var figure := x div trunc(exp(ln(10)*i)) mod 10;
      SetLength(vrem_arr[figure], vrem_arr[figure].Length+1);
      vrem_arr[figure][vrem_arr[figure].Length-1] := x;
    end;
  SetLength(arr, 0);
  for var k := 0 to rand-1 do
    foreach var j in vrem_arr[k] do begin
      count += 1;
      SetLength(arr, arr.Length+1);
      arr[arr.Length-1] := j;
    end;
  end;
end;

{Расчёска}

{Быстрая}

{Подсчётом}

{Деревом}

{Перемешиванием}

{Основной код}

procedure Form1.comboBox1_SelectedIndexChanged(sender: Object; e: EventArgs);
begin
end;

procedure Form1.button1_Click(sender: Object; e: EventArgs);
var arr: array of integer;
    kol_vo, n: integer;
    res: boolean;
    f: file of integer;
begin
  Label1.Visible := False;
  Label2.Visible := False;
  Label3.Visible := False;
  Label4.Visible := False;
  Label5.Visible := False;
  Label11.Visible := False;
  
  var sorts := ComboBox1.SelectedIndex;
  var arrays := ComboBox2.SelectedIndex;
  var types := ComboBox3.SelectedIndex;
  kol_vo := 0;
  res := True;
  var check_options := ((sorts in [1..17]) and (arrays in [1..3]) and (types in [1..3])) or (ComboBox1.Text = 'Болотная (только 10 эл.)');
  var check_files := System.IO.File.Exists('C:\PABCWork.NET\TEMP\Array64') and System.IO.File.Exists('C:\PABCWork.NET\TEMP\Array1000') and System.IO.File.Exists('C:\PABCWork.NET\TEMP\Array10000-100000');
  if check_options and check_files then
  begin
    case arrays of
      1: begin
        Reset(f, 'C:\PABCWork.NET\TEMP\Array64');
        n := 64;
        SetLength(arr, n);
        case types of
          1: begin
            For var i := 0 to n-1 do
            Read(f, arr[i]);
          end;
          2:begin
            Seek(f, n+1);
            For var i := 0 to n-1 do
              Read(f, arr[i]);
          end;
          3: begin
              Seek(f, 2*(n+1));
              For var i := 0 to n-1 do
                Read(f, arr[i]);
          end;
        end;
      CloseFile(f);
      end;
      2: begin
        Reset(f, 'C:\PABCWork.NET\TEMP\Array1000');
        n := 1000;
        SetLength(arr, n);
        case types of
          1: begin
            For var i := 0 to n-1 do
            Read(f, arr[i]);
          end;
          2:begin
            Seek(f, n+1);
            For var i := 0 to n-1 do
              Read(f, arr[i]);
          end;
          3: begin
              Seek(f, 2*(n+1));
              For var i := 0 to n-1 do
                Read(f, arr[i]);
            end;
        end;
      CloseFile(f);
      end;
      3: begin
        Reset(f, 'C:\PABCWork.NET\TEMP\Array10000-100000');
        n := 20000;
        SetLength(arr, n);
        case types of
          1: begin
            For var i := 0 to n-1 do
            Read(f, arr[i]);
          end;
          2:begin
            Seek(f, n+1);
            For var i := 0 to n-1 do
              Read(f, arr[i]);
          end;
          3: begin
              Seek(f, 2*(n+1));
              For var i := 0 to n-1 do
                Read(f, arr[i]);
          end;
        end;
      CloseFile(f);
      end;
    end;
    var check_arr: array of integer;
    
    SetLength(check_arr, n);
    for var i := 0 to n-1 do
      check_arr[i] := arr[i];
    
    var sorts_name := ComboBox1.SelectedItem.ToString;
    if sorts_name <> 'Болотная (только 10 эл.)' then
      Sort(check_arr);
    
    case sorts_name of
      'Пузырьком': begin
        arr := SortPus(arr, kol_vo);
        
        var i1: integer;
        
        for var i := 0 to n-1 do
          if arr[i] <> check_arr[i] then begin
            res := False;
            i1 := i;
            break;
          end;
        if res then begin
          Label4.Text := 'Массив успешно отсортирован!';
          Label5.Text :=  IntToStr(kol_vo);
        end
        else
          begin
            Label4.Text := 'Произошла ошибка в сортировке! '+'Элемент: ' + i1;
            Label5.Text := 'Ошибка!';
          end;
      end;
      
      'Болотная (только 10 эл.)': begin
        n := 10;
        SetLength(arr, n);
        SetLength(check_arr, n);
        Reset(f, 'C:\PABCWork.NET\TEMP\Array64');
        for var i := 0 to n-1 do begin
          Read(f, arr[i]);
          check_arr[i] := arr[i];
        end;
        CloseFile(f);
        Sort(check_arr);
        bogo(arr, kol_vo);
        
        var i1: integer;
        
        for var i := 0 to n-1 do
          if arr[i] <> check_arr[i] then begin
            res := False;
            i1 := i;
            break;
          end;
        if res then begin
          Label4.Text := 'Массив успешно отсортирован (10 элементов)!';
          Label5.Text :=  IntToStr(kol_vo);
        end
        else
          begin
            Label4.Text := 'Произошла ошибка в сортировке! '+'Элемент: ' + i1;
            Label5.Text := 'Ошибка!';
            Writeln(arr);
            Writeln(check_arr);
          end;
      end;
      
      'TimSort': begin
        tim_sort(arr, kol_vo);
        
        var i1: integer;
        
        for var i := 0 to n-1 do
          if arr[i] <> check_arr[i] then begin
            res := False;
            i1 := i; 
            break;
          end;
        if res then begin
          Label4.Text := 'Массив успешно отсортирован!';
          Label5.Text :=  IntToStr(kol_vo);
        end
        else
          begin
            Label4.Text := 'Произошла ошибка в сортировке! '+'Элемент: ' + i1;
            Label5.Text := 'Ошибка!';
            Writeln(arr);
            Writeln(check_arr);
          end;
      end;
      
      'Вставками': begin
        insertation_sort(arr, 0, n-1, kol_vo);
        
        var i1: integer;
        
        for var i := 0 to n-1 do
          if arr[i] <> check_arr[i] then begin
            res := False;
            i1 := i;
            break;
          end;
        if res then begin
          Label4.Text := 'Массив успешно отсортирован!';
          Label5.Text :=  IntToStr(kol_vo);
        end
        else
          begin
            Label4.Text := 'Произошла ошибка в сортировке! '+'Элемент: ' + i1;
            Label5.Text := 'Ошибка!';
            Writeln(arr);
            Writeln(check_arr);
          end;
      end;
    
    'Слиянием': begin
        merge_sort(arr, 0, n div 2, n-1, kol_vo);

        var i1: integer;
        
        for var i := 0 to n-1 do
          if arr[i] <> check_arr[i] then begin
            res := False;
            i1 := i;
            break;
          end;
        if res then begin
          Label4.Text := 'Массив успешно отсортирован!';
          Label5.Text :=  IntToStr(kol_vo);
        end
        else
          begin
            Label4.Text := 'Произошла ошибка в сортировке! '+'Элемент: ' + i1;
            Label5.Text := 'Ошибка!';
            Writeln(arr);
            Writeln(check_arr);
          end;
      end;
    
    'Шелла': begin
        shell_sort(arr, kol_vo);

        var i1: integer;
        
        for var i := 0 to n-1 do
          if arr[i] <> check_arr[i] then begin
            res := False;
            i1 := i;
            break;
          end;
        if res then begin
          Label4.Text := 'Массив успешно отсортирован!';
          Label5.Text :=  IntToStr(kol_vo);
        end
        else
          begin
            Label4.Text := 'Произошла ошибка в сортировке! '+'Элемент: ' + i1;
            Label5.Text := 'Ошибка!';
            Writeln(arr);
            Writeln(check_arr);
          end;
      end;
    
    'Методом выбора': begin
        input_sort(arr, kol_vo);

        var i1: integer;
        
        for var i := 0 to n-1 do
          if arr[i] <> check_arr[i] then begin
            res := False;
            i1 := i;
            break;
          end;
        if res then begin
          Label4.Text := 'Массив успешно отсортирован!';
          Label5.Text :=  IntToStr(kol_vo);
        end
        else
          begin
            Label4.Text := 'Произошла ошибка в сортировке! '+'Элемент: ' + i1;
            Label5.Text := 'Ошибка!';
            Writeln(arr);
            Writeln(check_arr);
          end;
      end;
    
    'Пирамидальная': begin
        piramid_sort(arr, n, kol_vo);

        var i1: integer;
        
        for var i := 0 to n-1 do
          if arr[i] <> check_arr[i] then begin
            res := False;
            i1 := i;
            break;
          end;
        if res then begin
          Label4.Text := 'Массив успешно отсортирован!';
          Label5.Text :=  IntToStr(kol_vo);
        end
        else
          begin
            Label4.Text := 'Произошла ошибка в сортировке! '+'Элемент: ' + i1;
            Label5.Text := 'Ошибка!';
            Writeln(arr);
            Writeln(check_arr);
          end;
      end;
    
    'Гномья': begin
        gnomesort(arr, kol_vo);

        var i1: integer;
        
        for var i := 0 to n-1 do
          if arr[i] <> check_arr[i] then begin
            res := False;
            i1 := i;
            break;
          end;
        if res then begin
          Label4.Text := 'Массив успешно отсортирован!';
          Label5.Text :=  IntToStr(kol_vo);
        end
        else
          begin
            Label4.Text := 'Произошла ошибка в сортировке! '+'Элемент: ' + i1;
            Label5.Text := 'Ошибка!';
            Writeln(arr);
            Writeln(check_arr);
          end;
      end;
    
    'Поразрядная': begin
        var ab := abs(min(arr));
        
        for var i := 0 to n-1 do begin
          arr[i] += ab;
          check_arr[i] := arr[i];
        end;
        
        radix_sort(arr, kol_vo);
        sort(check_arr);        
        
        var i1: integer;
        
        for var i := 0 to n-1 do
          if arr[i] <> check_arr[i] then begin
            res := False;
            i1 := i;
            break;
          end;
        if res then begin
          Label4.Text := 'Массив успешно отсортирован!';
          Label5.Text :=  IntToStr(kol_vo);
        end
        else
          begin
            Label4.Text := 'Произошла ошибка в сортировке! '+'Элемент: ' + i1;
            Label5.Text := 'Ошибка!';
            Writeln(arr);
            Writeln(check_arr);
          end;
      end;
    
    //здесь добавить
      
      else
        begin
        Label4.Text := 'Сортировка ещё не добавлена :(';
        Label5.Text := 'Ошибка!';
      end;
    end;
    
    Label1.Visible := True;
    Label3.Visible := True;
    Label4.Visible := True;
    Label5.Visible := True;
  end
  else if not check_files then begin
   Label4.Text := 'Массивы не сгенерированы!';
   Label5.Text := 'Ошибка! Необходимо сгенерировать массивы!';
    Label1.Visible := True;
    Label3.Visible := True;
    Label4.Visible := True;
    Label5.Visible := True;
  end
  else begin
    Label4.Text := '';
    Label5.Text := '';
    Label2.Visible := True;
  end;
end;

procedure Form1.label2_Click(sender: Object; e: EventArgs);
begin
  
end;

procedure Form1.label4_Click(sender: Object; e: EventArgs);
begin
  
end;

procedure Form1.comboBox2_SelectedIndexChanged(sender: Object; e: EventArgs);
begin
end;

procedure Form1.label6_Click(sender: Object; e: EventArgs);
begin
  
end;

procedure Form1.button2_Click(sender: Object; e: EventArgs);
begin
  ComboBox1.Visible := True;
  ComboBox2.Visible := True;
  ComboBox3.Visible := True;
  Label6.Visible := True;
  Label7.Visible := True;
  Label8.Visible := True;
  Button1.Visible := True;
  Button3.Visible := True;
  Button6.Visible := True;
  
  Label9.Visible := False;
  Button2.Visible := False;
end;

procedure Form1.button3_Click(sender: Object; e: EventArgs);
begin
  ComboBox1.Visible := False;
  ComboBox2.Visible := False;
  ComboBox3.Visible := False;
  Label1.Visible := False;
  Label2.Visible := False;
  Label3.Visible := False;
  Label4.Visible := False;
  Label5.Visible := False;
  Label6.Visible := False;
  Label7.Visible := False;
  Label8.Visible := False;
  Label11.Visible := False;
  Button1.Visible := False;
  Button3.Visible := False;
  Button6.Visible := False;
  
  Label10.Visible := True;
  Button4.Visible := True;
  Button5.Visible := True;
end;

procedure Form1.button4_Click(sender: Object; e: EventArgs);
begin
  ComboBox1.Visible := True;
  ComboBox2.Visible := True;
  ComboBox3.Visible := True;
  Label6.Visible := True;
  Label7.Visible := True;
  Label8.Visible := True;
  Button1.Visible := True;
  Button3.Visible := True;
  Button6.Visible := True;
  if label5.Text <> '' then
  begin
    Label1.Visible := True;
    Label3.Visible := True;
    Label4.Visible := True;
    Label5.Visible := True;
  end;
  
  Label10.Visible := False;
  Button4.Visible := False;
  Button5.Visible := False;
end;

procedure Form1.button5_Click(sender: Object; e: EventArgs);
begin
  Close;
end;

procedure Form1.label10_Click(sender: Object; e: EventArgs);
begin
  
end;

procedure Form1.button6_Click(sender: Object; e: EventArgs);
begin
  var f: file of integer;
  var t: PABCSystem.text;
  
  Label1.Visible := False;
  Label2.Visible := False;
  Label3.Visible := False;
  Label4.Visible := False;
  Label5.Visible := False;
  Label11.Visible := True;
  if not(System.IO.Directory.Exists('C:\PABCWork.NET\TEMP')) then
    System.IO.Directory.CreateDirectory('C:\PABCWork.NET\TEMP');
  Rewrite(t, 'C:\PABCWork.NET\TEMP\Массивы.txt');
  Writeln(t, 'ВНИМАНИЕ! ДЛЯ БОЛОТНОЙ СОРТИРОВКИ БЕРЁТСЯ ТОЛЬКО 10 ЭЛЕМЕНТОВ ЛУЧШЕГО СЛУЧАЯ НА 64 ЭЛЕМЕНТА!!!');
  Writeln(t);
  Rewrite(f, 'C:\PABCWork.NET\TEMP\Array64', Encoding.Default);
  Writeln(t,'64 элемента');
  Writeln(t);
  Writeln(t, 'Лучший случай:');
  Writeln(t);
  for var i := -32 to 31 do begin
    var j :=i+PABCSystem.random(-5,5);
    Write(f,j);
    Write(t,j, ' ');
  end;
  Writeln(t);
  Write(F, -1000000);
  Writeln(t);
  Writeln(t, 'Средний случай:');
  Writeln(t);
  for var i := -32 to 31 do begin
    var j :=i+PABCSystem.random(-64, 64);
    Write(f,j);
    Write(t,j, ' ');
  end;
  Writeln(t);
  Write(F, -1000000);
  Writeln(t);
  Writeln(t, 'Худший случай:');
  Writeln(t);
  for var i := 31 downto -32 do begin
    var j :=i+PABCSystem.random(-5,5);
    Write(f,j);
    Write(t,j, ' ');
  end;
  {Writeln(t);
  Write(f, -1000000);
  Writeln(t, 'Массив для поразрядной сортировки');
  Writeln(t);
  for var i := 0 to 63 do begin
    var j := i+PABCSystem.Random(0,10);
    Write(f, j);
    Write(t, j, ' ');
  end;}
  Writeln(t);
  Writeln(t,'_'*1000);
  Writeln(t);
  CloseFile(f);
  Rewrite(f, 'C:\PABCWork.NET\TEMP\Array1000');
  Writeln(t, '1000 элементов');
  Writeln(t);
  Writeln(t, 'Лучший случай:');
  Writeln(t);
  for var i := -500 to 499 do begin
    var j :=i+PABCSystem.random(-10,10);
    Write(f,j);
    Write(t,j, ' ');
  end;
  Writeln(t);
  Write(F, -1000000);
  Writeln(t);
  Writeln(t, 'Средний случай:');
  Writeln(t);
  for var i := -500 to 499 do begin
    var j :=i+PABCSystem.random(-1000,1000);
    Write(f,j);
    Write(t,j, ' ');
  end;
  Writeln(t);
  Write(F, -1000000);
  Writeln(t);
  Writeln(t, 'Худший случай:');
  Writeln(t);
  for var i := 499 downto -500 do begin
    var j :=i+PABCSystem.random(-10,10);
    Write(f,j);
    Write(t,j, ' ');
  end;
  {Writeln(t);
  Write(f, -1000000);
  Writeln(t, 'Массив для поразрядной сортировки');
  Writeln(t);
  for var i := 0 to 999 do begin
    var j := i+PABCSystem.Random(0,20);
    Write(f, j);
    Write(t, j, ' ');
  end;}
  Writeln(t);
  Writeln(t,'_'*1000);
  Writeln(t);
  CloseFile(f);
  Rewrite(f, 'C:\PABCWork.NET\TEMP\Array10000-100000');
  Writeln(t, '10000-100000 элементов');
  Writeln(t);
  Writeln(t, 'Лучший случай:');
  Writeln(t);
  for var i := -10000 to 9999 do begin
    var j :=i+PABCSystem.random(-50,50);
    Write(f,j);
    Write(t,j, ' ');
  end;
  Writeln(t);
  Write(F, -1000000);
  Writeln(t);
    Writeln(t, 'Средний случай:');
  Writeln(t);
  for var i := -10000 to 9999 do begin
    var j :=i+PABCSystem.random(-10000,9999);
    Write(f,j);
    Write(t,j, ' ');
  end;
  Writeln(t);
  Write(F, -1000000);
  Writeln(t);
  Writeln(t, 'Худший случай:');
  Writeln(t);
  for var i := 9999 downto -10000 do begin
    var j :=i+PABCSystem.random(-50,50);
    Write(f,j);
    Write(t,j, ' ');
  end;
  {Writeln(t);
  Write(f, -1000000);
  Writeln(t, 'Массив для поразрядной сортировки');
  Writeln(t);
  for var i := 0 to 19999 do begin
    var j := i+PABCSystem.Random(0,100);
    Write(f, j);
    Write(t, j, ' ');
  end;}
  CloseFile(f);
  CloseFile(t);
end;

procedure Form1.label11_Click(sender: Object; e: EventArgs);
begin
  
end;

end.